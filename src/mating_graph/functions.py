from src.piece import Piece
from src.mating_graph.internals import get_anchors_from_piece_segmentation,MatingGraph

def bulid_graph(pieces:list[Piece]):
    anchors = get_anchors_from_piece_segmentation(pieces)
    graph = MatingGraph(anchors)

    return graph

def compatability_overlapping(graph:MatingGraph):
    pass