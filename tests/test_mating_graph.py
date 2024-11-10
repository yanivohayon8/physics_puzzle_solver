import unittest
from src.mating_graph.internals import AnchorConf
from src.piece import Piece
from PIL import Image,ImageDraw
from src.mating_graph import internals
from src.mating_graph import functions
import matplotlib.pyplot as plt

class TestInternals(unittest.TestCase):
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
        
        graph = internals.MatingGraph(anchors_confs)
        graph.draw()

        plt.show()


class TestBuildingGraph(unittest.TestCase):

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

        graph = functions.bulid_graph([square,triangle])
        graph.draw()

        plt.show()








if __name__ == "__main__":
    unittest.main()