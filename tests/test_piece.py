import unittest
# import sys
# sys.path.append("..")

from src.piece import Piece
from PIL import Image
import matplotlib.pyplot as plt

class TestPiece(unittest.TestCase):

    def test_contour(self):
        image = Image.open("tests/data/RPf_00316_intact_mesh.png")
        piece = Piece(None,image)

        _, ax = plt.subplots()
        piece.draw_contour(ax=ax)
        plt.show()



if __name__ == "__main__":
    unittest.main()
