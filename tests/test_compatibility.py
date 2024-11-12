import unittest
from shapely import Polygon
from src import compatibilities
import matplotlib.pyplot as plt

class TestOverlapping(unittest.TestCase):

    def test_square_triangle(self):
        triangle = Polygon([(64, 24), (24, 104), (104, 104)])
        square = Polygon( [(34, 34), (34, 94), (94, 94), (94, 34)])    
        polygons = [triangle,square]
        overlapping = compatibilities.semi_dice_overlapping(polygons)
        
        xs,ys = triangle.exterior.xy
        plt.fill(xs,ys,facecolor="lightsalmon")
        xs,ys = square.exterior.xy
        plt.fill(xs,ys,facecolor="blue")
        plt.show()
        
        assert overlapping > 1


if __name__ == "__main__":
    unittest.main()