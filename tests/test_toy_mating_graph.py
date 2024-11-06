import unittest
from src.piece import Piece
from PIL import Image
from src.mating_graph.anchoring import AnchorConf
from src.mating_graph import mating_graph
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    unittest.main()