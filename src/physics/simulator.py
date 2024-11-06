import urllib3
import json
from urllib.parse import urlencode
import numpy as np

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
            degrees*=-1
            self.piece_id2transformation[trans_json["pieceId"]] = {"tx":tx,"ty":ty,"rot_degrees":degrees}

    def get_transformations(self)->dict:
        return self.piece_id2transformation