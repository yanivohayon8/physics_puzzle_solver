import unittest
from src import piece as piece_module
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

class TestPiece(unittest.TestCase):
    def test_contour(self):
        image = Image.open("tests/data/RPf_00316_intact_mesh.png")
        piece = piece_module.Piece(0,image)

        _, ax = plt.subplots()
        piece.draw_contour(ax=ax)
        plt.show()
    
    def create_polygon_image_(self,width, height, vertices:list,fill_color="white"):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        # Draw the polygon
        draw.polygon(vertices, fill=fill_color)

        return image

    def test_triangle_square(self):
        image_size = (128,128)
        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        triangle_image = self.create_polygon_image_(*image_size, triangle_vertices )
        square_image = self.create_polygon_image_(*image_size,square_vertices )

        triangle = piece_module.Piece("triangle",triangle_image)
        square = piece_module.Piece("square",square_image)

        _, axs = plt.subplots(2,2)

        triangle_contour = triangle.get_contour(format="list")
        square_contour = square.get_contour(format="list")
        
        axs[0,0].imshow(triangle_image)
        axs[0,1].imshow(self.create_polygon_image_(*image_size, triangle_contour ))
        axs[1,0].imshow(square_image)
        axs[1,1].imshow(self.create_polygon_image_(*image_size, square_contour ))

        plt.show()
    


class TestContourSegmentation(unittest.TestCase):
    def test_segmentation_by_threshold(self):
        image = Image.open("tests/data/RPf_00316_intact_mesh.png")
        piece = piece_module.Piece(0,image)

        polygon = piece.get_contour()
        segmenting_points, segmenting_indices = piece.segment_contour()
        curvatures = piece_module.compute_scaled_points_curvature_(polygon)
        xs = piece_module.get_polygon_xs(polygon)
        ys = piece_module.get_polygon_ys(polygon)

        plt.plot(xs,ys,label="Curve")
        norm = Normalize()
        colors = plt.cm.hot(norm(curvatures))

        plt.scatter(xs,ys,c=colors,label='points',cmap="hot")
        cbar = plt.colorbar()
        cbar.set_label("Curvature")

        segmenting_xs = piece_module.get_polygon_xs(segmenting_points)
        segmenting_ys = piece_module.get_polygon_ys(segmenting_points)

        plt.scatter(segmenting_xs,segmenting_ys,marker="X",linewidths=1.5,color="black")
        plt.axis("equal")
        plt.gca().invert_yaxis()

        plt.legend()
        plt.title('Polygon with Curvature Visualization')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()

class TestPolygon(unittest.TestCase):
    def test_polygon_edges_as_tuples(self):
        square = np.array([
            [0,0],
            [10,0],
            [10,10],
            [0,10]
        ])

        edges = piece_module.get_edges_as_tuples_list(square)

        assert len(edges) == 4

if __name__ == "__main__":
    unittest.main()
