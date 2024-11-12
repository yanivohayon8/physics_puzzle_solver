import unittest
from src.mating_graph.internals import AnchorConf,simulate_reconstruction_
from src.piece import Piece
from PIL import Image,ImageDraw
from src.mating_graph import internals
from src.mating_graph import functions
import matplotlib.pyplot as plt

def create_polygon_image_(width, height, vertices:list,fill_color="white"):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    draw.polygon(vertices, fill=fill_color)

    return image

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

    def test_get_link(self):
        width, height = 128, 128
        triangle = Piece("triangle",create_polygon_image_(width, height,[(64, 24), (24, 104), (104, 104)]))
        square = Piece("square",create_polygon_image_(width, height,[(34, 34), (34, 94), (94, 94), (94, 34)]))
        
        anchor1 = AnchorConf([[64, 24]] ,triangle)
        anchor2 = AnchorConf([[34, 34]] ,square)
        anchors_confs =[anchor1,anchor2]
        graph = internals.MatingGraph(anchors_confs)
        
        link_1 = graph.get_link_data(node1=anchor1,node2=anchor2)
        assert isinstance(link_1,dict)
        print(link_1)

        link_2 = graph.get_link_data((repr(anchor1),repr(anchor2)))
        assert isinstance(link_2,dict)
        print(link_2)

        assert link_1 == link_2

    def test_simulations_links(self):
        width, height = 128, 128
        triangle = Piece("triangle",create_polygon_image_(width, height,[(64, 24), (24, 104), (104, 104)]))
        square = Piece("square",create_polygon_image_(width, height,[(34, 34), (34, 94), (94, 94), (94, 34)]))
        anchors_confs =[AnchorConf([[64, 24]] ,triangle),AnchorConf([[34, 34]] ,square)]

        graph = internals.MatingGraph(anchors_confs)
        link = graph.get_as_link_tuple_(anchors_confs[0],anchors_confs[1])
        data_before = graph.get_link_data(link)
        response = graph.get_link_simulation_response_(link)

        assert data_before != graph.get_link_data(link).keys()

        assembly_image = response.restore_image([triangle,square])
        plt.imshow(assembly_image)
        plt.show()
    
    def test_aligned_polygons(self):
        width, height = 128, 128
        triangle = Piece("triangle",create_polygon_image_(width, height,[(64, 24), (24, 104), (104, 104)]))
        square = Piece("square",create_polygon_image_(width, height,[(34, 34), (34, 94), (94, 94), (94, 34)]))
        anchors_confs =[AnchorConf([[64, 24]] ,triangle),AnchorConf([[34, 34]] ,square)]

        graph = internals.MatingGraph(anchors_confs)
        link = graph.get_as_link_tuple_(anchors_confs[0],anchors_confs[1])

        _, axs = plt.subplots(1,2)

        response = graph.get_link_simulation_response_(link)
        assembly_image = response.restore_image([triangle,square])
        axs[0].imshow(assembly_image)

        aligned_polygons = graph.get_aligned_polygons_(link)
        xs,ys = aligned_polygons[0].exterior.xy
        axs[1].fill(xs,ys,facecolor="lightsalmon")
        xs,ys = aligned_polygons[1].exterior.xy
        axs[1].fill(xs,ys,facecolor="blue")

        plt.show()





    def test_simulation(self):
        width, height = 128, 128
        triangle = Piece("triangle",create_polygon_image_(width, height,[(64, 24), (24, 104), (104, 104)]))
        square = Piece("square",create_polygon_image_(width, height,[(34, 34), (34, 94), (94, 94), (94, 34)]))
        anchor1 = AnchorConf([[64, 24]] ,triangle)
        anchor2 = AnchorConf([[34, 34]] ,square)

        response = simulate_reconstruction_(anchor1,anchor2)
        assembly_image = response.restore_image([triangle,square])

        plt.imshow(assembly_image)
        plt.show()



class TestBuildingGraph(unittest.TestCase):

    def test_get_anchors_from_segmenting(self):
        width, height = 128, 128

        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        triangle_image = create_polygon_image_(width, height, triangle_vertices)
        triangle = Piece("triangle",triangle_image)

        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        square_image = create_polygon_image_(width, height, square_vertices)
        square = Piece("square",square_image)

        graph = functions.bulid_graph([square,triangle])
        graph.draw()

        plt.show()








if __name__ == "__main__":
    unittest.main()