from src.piece import Piece
from src.mating_graph.internals import get_anchors_from_piece_segmentation,MatingGraph
from src import compatibilities

def bulid_graph(pieces:list[Piece]):
    anchors = get_anchors_from_piece_segmentation(pieces)
    graph = MatingGraph(anchors)

    return graph

def compatability_overlapping(graph:MatingGraph):
    for link in graph.get_inter_piece_links():
        polygons = graph.get_aligned_polygons(link)
        overlap_score = compatibilities.semi_dice_overlapping(polygons)
        graph.update_compatibility(link,"semi_dice_overlapping",overlap_score)
