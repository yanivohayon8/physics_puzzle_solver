import unittest
from src.physics import simulator
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from src.piece import Piece

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



class TestRestorer(unittest.TestCase):

    
    def create_polygon_image_(self,width, height, vertices:list,fill_color="white"):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        # Draw the polygon
        draw.polygon(vertices, fill=fill_color)

        return image


    def test_create_polygon_image(self):
        width, height = 128, 128
        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        triangle_image = self.create_polygon_image_(width, height, triangle_vertices)
        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        square_image = self.create_polygon_image_(width, height, square_vertices)
        _,axs = plt.subplots(1,2)
        axs[0].imshow(triangle_image)
        axs[1].imshow(square_image)

        plt.show()


    def test_build_puzzle_from_response(self):
        image_size = (128,128)
        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        triangle_image = self.create_polygon_image_(*image_size, triangle_vertices )
        square_image = self.create_polygon_image_(*image_size,square_vertices,fill_color="gray" )

        triangle = Piece("trianlge",triangle_image)
        squre = Piece("square",square_image)
        pieces = [triangle,squre]

        # The request - you can use postman to restore the results (the expected image)
        '''
                        {
                "pieces": [
                    {
                        "id": "trianlge",
                        "polygon": [
                            [
                                63,
                                24
                            ],
                            [
                                24,
                                104
                            ],
                            [
                                104,
                                104
                            ],
                            [
                                65,
                                24
                            ]
                        ]
                    },
                    {
                        "id": "square",
                        "polygon": [
                            [
                                34,
                                34
                            ],
                            [
                                34,
                                94
                            ],
                            [
                                94,
                                94
                            ],
                            [
                                94,
                                34
                            ]
                        ]
                    }
                ],
                "matings": [
                    {
                        "firstPiece": "trianlge",
                        "firstPieceLocalCoords": [
                            64,
                            24
                        ],
                        "secondPiece": "square",
                        "secondPieceLocalCoords": [
                            34,
                            34
                        ]
                    }
                ]
            }
        '''

        res_json ={
            "piecesFinalCoords": [
                {
                    "coordinates": [
                        [
                            63.0,
                            24.0
                        ],
                        [
                            24.0,
                            104.00000762939453
                        ],
                        [
                            104.00000762939453,
                            104.00000762939453
                        ],
                        [
                            65.00000762939453,
                            24.0
                        ]
                    ],
                    "pieceId": "trianlge"
                },
                {
                    "coordinates": [
                        [
                            64.08230590820313,
                            23.28544044494629
                        ],
                        [
                            107.93525695800781,
                            -17.664777755737305
                        ],
                        [
                            66.98501586914063,
                            -61.5177116394043
                        ],
                        [
                            23.1320858001709,
                            -20.56749153137207
                        ]
                    ],
                    "pieceId": "square"
                }
            ],
            "piecesFinalTransformations": [
                {
                    "pieceId": "trianlge",
                    "rotationRadians": 0.0,
                    "translateVectorX": 64.00000762939453,
                    "translateVectorY": 64.00000762939453
                },
                {
                    "pieceId": "square",
                    "rotationRadians": -2.32197904586792,
                    "translateVectorX": 65.53366088867188,
                    "translateVectorY": -19.116134643554688
                }
            ]
        }

        response = simulator.Response(res_json)
        assembly_image = response.restore_image(pieces)

        plt.imshow(assembly_image)
        plt.show()


    def test_integrated_reconstruction(self):
        image_size = (128,128)
        triangle_vertices = [(64, 24), (24, 104), (104, 104)]
        square_vertices = [(34, 34), (34, 94), (94, 94), (94, 34)]
        triangle_image = self.create_polygon_image_(*image_size, triangle_vertices )
        square_image = self.create_polygon_image_(*image_size,square_vertices,fill_color="gray" )

        triangle = Piece("trianlge",triangle_image)
        squre = Piece("square",square_image)
        pieces = [triangle,squre]

        matings =[{
                "firstPiece":"trianlge",
                "firstPieceLocalCoords": (64, 24),
                "secondPiece":"square",
                "secondPieceLocalCoords": (34, 34)
        }]

        pieces_json = [simulator.build_piece_json(piece.get_id(),piece.get_contour()) for piece in pieces]
        response = simulator.send_reconstruction(pieces_json,matings,reconstruction_params={"visibilityOn":1})
        assembly_image = response.restore_image(pieces)

        plt.imshow(assembly_image)
        plt.show()

    


if __name__ == "__main__":
    unittest.main()