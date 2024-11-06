from src.piece import Piece,get_edges_as_tuples_list
from src.mating_graph.anchoring import edges_as_anchor_confs

def get_anchors_from_piece_segmentation_(pieces:list[Piece]):
    total_anchors = []

    for piece in pieces:
        segmenting_points, _ = piece.segment_contour()
        edges_1 = get_edges_as_tuples_list(segmenting_points)
        anchors = edges_as_anchor_confs(edges_1,piece)
        total_anchors+= anchors

        # to exploit the 4 permutations of attaching two pieces
        total_anchors+= [anchor.reversed() for anchor in anchors]

    return total_anchors