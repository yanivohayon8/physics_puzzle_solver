from src.piece import Piece
from src.mating_graph.internals import get_anchors_from_piece_segmentation_,MatingGraph

def bulid_graph(pieces:list[Piece]):
    anchors = get_anchors_from_piece_segmentation_(pieces)
    graph = MatingGraph(anchors)

    return graph