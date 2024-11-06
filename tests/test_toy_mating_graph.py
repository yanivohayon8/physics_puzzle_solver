import unittest
from src.piece import Piece,get_edges_as_tuples_list
from PIL import Image
from src.mating_graph.anchoring import AnchorConf,edges_as_anchor_confs
from src.mating_graph import mating_graph
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







if __name__ == "__main__":
    unittest.main()