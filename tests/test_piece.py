import unittest
# import sys
# sys.path.append("..")

from src import piece as piece_module
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

class TestPiece(unittest.TestCase):
    def test_contour(self):
        image = Image.open("tests/data/RPf_00316_intact_mesh.png")
        piece = piece_module.Piece(0,image)

        _, ax = plt.subplots()
        piece.draw_contour(ax=ax)
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

if __name__ == "__main__":
    unittest.main()
