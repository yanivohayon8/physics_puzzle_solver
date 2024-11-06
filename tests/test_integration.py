import unittest
from src.piece import Piece,get_edges_as_tuples_list
from PIL import Image,ImageDraw
from src.mating_graph.anchoring import AnchorConf,edges_as_anchor_confs
from src.mating_graph import mating_graph
from src.mating_graph.build import get_anchors_from_piece_segmentation_
import matplotlib.pyplot as plt
import numpy as np


class TestIntegrationToy(unittest.TestCase):

    def create_polygon_image_(self,width, height, vertices:list,fill_color="white"):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        draw.polygon(vertices, fill=fill_color)

        return image

    def test_square_triangle(self):
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