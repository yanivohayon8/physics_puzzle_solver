import urllib3
import json
from urllib.parse import urlencode
import numpy as np
from src.piece import Piece
from src import mask_background
from PIL import Image
from shapely import Polygon

host_="localhost"
port_ = 8888
http_ = urllib3.PoolManager()
url_prefix_ = "v1"
base_target_ = f"http://{host_}:{port_}/{url_prefix_}"

def init(host="localhost", port=8888):
    global host_
    global port_
    global url_prefix_
    global base_target_

    host_= host
    port_ = port
    url_prefix_ = "v1"
    base_target_ = f"http://{host_}:{port_}/{url_prefix_}"


def send_sanity():
    global base_target_
    global http_

    target = f"{base_target_}/sanity"
    response = http_.request('GET', target)

    if response.status != 200:
        raise Exception(response.reason)

    return response.data.decode('utf-8')

def send_request_(body,headers,**params):
    global base_target_
    global http_

    encoded_args = urlencode(params)
    query_parameters_str = "reconstructions?" + encoded_args
    target = f"{base_target_}/{query_parameters_str}"

    response = http_.request(
        'POST',
        target,
        body=body,
        headers=headers
    )

    return json.loads(response.data.decode('utf-8'))

def send_reconstruction(pieces,matings,headers={'Content-Type': 'application/json'},**params):
    body = {
        "pieces":pieces,
        "matings": matings
    }

    encoded_body = json.dumps(body)
    res_json = send_request_(encoded_body,headers,**params)

    return Response(res_json)


def build_mating_json(piece_id1:str,local_coords_1:list,piece_id2:str,local_coords_2:list):
    return {
        "firstPiece":piece_id1,
        "firstPieceLocalCoords": local_coords_1,
        "secondPiece":piece_id2,
        "secondPieceLocalCoords": local_coords_2
    }

def build_piece_json(piece_id,contour_polygon):
    contour = contour_polygon

    if isinstance(contour_polygon,np.ndarray):
        contour = contour_polygon.tolist()

    return {
            "id": piece_id,
            "polygon":contour
    }

class Response():

    def __init__(self,response_json) -> None:
        self.response_json = response_json
        self.piece_id2transformation = {}

        for trans_json in response_json["piecesFinalTransformations"]:
            tx = int(trans_json["translateVectorX"])
            ty = int(trans_json["translateVectorY"])
            degrees = np.rad2deg(trans_json["rotationRadians"])
            self.piece_id2transformation[trans_json["pieceId"]] = {"tx":tx,"ty":ty,"rot_degrees":degrees}

    def get_transformations(self)->dict:
        return self.piece_id2transformation
    
    def get_final_polygons(self,out_format="tuples")->list:
        pieces_coordinates = [piece_json["coordinates"] for piece_json in self.response_json["piecesFinalCoords"]]

        if out_format == "shapely":
            return [Polygon(coords) for coords in pieces_coordinates]
        else:
            return pieces_coordinates

    def restore_image(self,pieces:list[Piece],background_mode="RGB",background_size=(224,224)):
        background_img = Image.new(background_mode,background_size)

        for piece in pieces:
            transformation = self.get_transformations()[piece.get_id()]
            piece_img_rotated = piece.get_image().rotate(transformation["rot_degrees"]) # should I put minus here? it should be processed in the rotation earlier...

            if piece.get_image().mode == "RGBA":
                piece_mask = mask_background.mask_background_rgba(piece_img_rotated) 
            elif piece.get_image().mode == "L":
                piece_mask = mask_background.mask_background_grayscale(piece_img_rotated) 
            elif piece.get_image().mode == "RGB":
                piece_mask = mask_background.mask_background_rgb(piece_img_rotated)
            else:
                raise NotImplementedError(f"Implement mask transperancy thresholding for {piece.get_image().mode}...")

            background_img.paste(piece_img_rotated,box=(transformation["tx"],transformation["ty"]),mask=piece_mask)

        return background_img