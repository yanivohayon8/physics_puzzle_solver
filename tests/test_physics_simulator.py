import unittest
from src.physics import simulator
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np

class TestSimulator(unittest.TestCase):

    def test_sanity(self):
        response = simulator.send_sanity()

        print(response)
        assert "Hello World" in response
    
    def test_simple_reconstruction(self):
        pieces = [
        {
            "id": "square",
            "polygon":[[500,500],[-500,500],[-500,-500],[500,-500]]
        },
        {
            "id": "triangle",
            "polygon":[[500,500],[-500,500],[-500,-500]]
        }
        ]
        
        matings = [
            {
                "firstPiece":"square",
                "firstPieceLocalCoords": [-500,500],
                "secondPiece":"triangle",
                "secondPieceLocalCoords": [500,500]
            }
            ,{
                "firstPiece":"square",
                "firstPieceLocalCoords": [500,500], 
                "secondPiece":"triangle",
                "secondPieceLocalCoords": [-500,500] 
            }
        ]

        response = simulator.send_reconstruction(pieces,matings)

        assert isinstance(response.get_transformations(),dict)
    
    def test_simple_reconstruction_visibility(self):
        pieces = [
        {
            "id": "square",
            "polygon":[[500,500],[-500,500],[-500,-500],[500,-500]]
        },
        {
            "id": "triangle",
            "polygon":[[500,500],[-500,500],[-500,-500]]
        }
        ]
        
        matings = [
            {
                "firstPiece":"square",
                "firstPieceLocalCoords": [-500,500],
                "secondPiece":"triangle",
                "secondPieceLocalCoords": [500,500]
            }
            ,{
                "firstPiece":"square",
                "firstPieceLocalCoords": [500,500], 
                "secondPiece":"triangle",
                "secondPieceLocalCoords": [-500,500] 
            }
        ]

        response = simulator.send_reconstruction(pieces,matings,visibilityOn=1)

        assert isinstance(response.get_transformations(),dict)





    


if __name__ == "__main__":
    unittest.main()