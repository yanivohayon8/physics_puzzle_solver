import unittest
from src.piece import Piece
from PIL import Image,ImageDraw
from src.mating_graph import functions


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

        graph = functions.bulid_graph([square,triangle])

        

if __name__ == "__main__":
    unittest.main()