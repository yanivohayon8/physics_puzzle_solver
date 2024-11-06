import unittest
from src.piece import Piece,get_edges_as_tuples_list
from PIL import Image,ImageDraw
from src.mating_graph.anchoring import AnchorConf,edges_as_anchor_confs
from src.mating_graph import mating_graph
from src.mating_graph.build import get_anchors_from_piece_segmentation_
import matplotlib.pyplot as plt
import numpy as np

class TestToyMatingGraph(unittest.TestCase):
    def test_init_graph(self):
        blank_image = Image.new("L",(100,100))
        piece1 = Piece("0",blank_image,contour_polygon=[])
        piece2 = Piece("1",blank_image,contour_polygon=[])

        anchors_confs = [
            AnchorConf([[734.4363693319759,1006.955673897721]] ,piece1),
            AnchorConf([[270.8407352941176,384.5944117647059]] ,piece1),
            AnchorConf([[66.6498978473929, 439.4158647440263]] ,piece2),
            AnchorConf([[683.2693400246188, 1164.8895464444654]] ,piece2)
        ]
        
        mating_graph.initGraph(anchors_confs)
        mating_graph.draw()

        plt.show()

    def test_integration_to_segmentation(self):
        piece1 = Piece("1",None,contour_polygon=[])
        segmenting_points_1 = np.array([[ 727,  945],[1025, 1267],[1247,  894]])
        edges_1 = get_edges_as_tuples_list(segmenting_points_1)
        anchors1 = edges_as_anchor_confs(edges_1,piece1)

        piece2 = Piece("2",None,contour_polygon=[])
        segmenting_points_2 = np.array([[1025, 1267],[1247,  894],[ 869,  784]])
        edges_2 = get_edges_as_tuples_list(segmenting_points_2)
        anchors2 = edges_as_anchor_confs(edges_2,piece2)

        total_anchors = anchors1+anchors2
        mating_graph.initGraph(total_anchors)
        mating_graph.draw()

        plt.show()
    
    def create_polygon_image_(self,width, height, vertices:list,fill_color="white"):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        draw.polygon(vertices, fill=fill_color)

        return image

    def test_get_anchors_from_segmenting(self):
        width, height = 128, 128

        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        triangle_image = self.create_polygon_image_(width, height, triangle_vertices)
        triangle = Piece("triangle",triangle_image)

        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        square_image = self.create_polygon_image_(width, height, square_vertices)
        square = Piece("square",square_image)

        anchors = get_anchors_from_piece_segmentation_([triangle,square])
        mating_graph.initGraph(anchors)
        mating_graph.draw()

        plt.show()








if __name__ == "__main__":
    unittest.main()