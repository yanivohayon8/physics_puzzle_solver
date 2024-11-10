from functools import reduce
import networkx as nx
import matplotlib.pyplot as plt
from src.piece import Piece
from src.physics import simulator


class AnchorConf():

    def __init__(self,anchor_points:list,parent_piece:Piece,**metadata) -> None:
        '''
            anchor_points - list of tuples of numbers  - the order in the list matters! (it determines the permutation)
            parent_piece - piece to be anchored
        '''
        assert isinstance(anchor_points,(list,tuple))
        self.anchor_points_ = anchor_points
        self.parent_piece_ = parent_piece
        self.__dict__.update(metadata)

    def __repr__(self) -> str:
        points_concatenated = reduce(lambda acc,x: acc+"&"+str(x),self.anchor_points_,"")
        return f"{repr(self.parent_piece_)}-{points_concatenated}"

    def get_num_anchors(self):
        return len(self.anchor_points_)

    def get_parent_piece(self):
        return self.parent_piece_
    
    def get_points(self):
        return self.anchor_points_

    def reversed(self):
        return AnchorConf(list(reversed(self.anchor_points_)),self.parent_piece_)

class MatingGraph():
    PAIRING_DELIMITER = "<=>"
    DRAWING_STRONG_CONNECTION = 1
    DRAWING_WEAK_CONNECTION = 0.5

    LINK_TYPE_SAME_PIECE = "same_piece"
    LINK_TYPE_INTER_PIECE = "inter_piece"

    def __init__(self,anchor_confs: list[AnchorConf]):
        self.graph_ = nx.Graph()
        self.piece2node_ = {}
        self.drawing_pos_ = {}

        for conf in anchor_confs:
            assert isinstance(conf, AnchorConf)

        self.graph_ = nx.Graph()

        for conf in anchor_confs:
            self.graph_.add_node(repr(conf), conf=conf)

        for ii, conf1 in enumerate(anchor_confs):
            for conf2 in anchor_confs[ii+1:]:
                edge_type = self.LINK_TYPE_SAME_PIECE
                pos_weight = self.DRAWING_STRONG_CONNECTION

                if conf1.get_parent_piece() != conf2.get_parent_piece():
                    edge_type = self.LINK_TYPE_INTER_PIECE
                    pos_weight = self.DRAWING_WEAK_CONNECTION

                self.graph_.add_edge(repr(conf1), repr(conf2), edge_type=edge_type, pos_weight=pos_weight)

        pos_tmp = nx.shell_layout(self.graph_)
        self.drawing_pos_ = nx.kamada_kawai_layout(self.graph_, pos=pos_tmp, weight="pos_weight")

    def get_inter_piece_edges_(self, is_data=True):
        graph_links = self.graph_.edges(data=True)

        if is_data:
            return [(u, v, data) for u, v, data in graph_links if data["edge_type"] == self.LINK_TYPE_INTER_PIECE]
        else:
            return [(u, v) for u, v, data in graph_links if data["edge_type"] == self.LINK_TYPE_INTER_PIECE]

    def get_interpiece_links_to_anchors_(self) -> dict:
        graph_links = self.graph_.edges(data=True)
        pairs = {}

        for u, v, data in graph_links:
            if data["edge_type"] == self.LINK_TYPE_INTER_PIECE:
                data_u = self.graph_.nodes[u]
                data_v = self.graph_.nodes[v]
                pairs[(u, v)] = (data_u["conf"], data_v["conf"])

        return pairs

    def get_node_data_(self, node):
        return self.graph_.nodes[node]

    def draw(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.subplot()

        pos_spaced = self.drawing_pos_

        nx.draw_networkx_nodes(self.graph_, pos=pos_spaced, node_color="skyblue", ax=ax)
        nx.draw_networkx_labels(self.graph_, pos=pos_spaced, font_size=8, font_color='black', ax=ax)

        graph_links = self.graph_.edges(data=True)
        inter_piece_links = []
        same_piece_links = []

        for u, v, data in graph_links:
            if data["edge_type"] == self.LINK_TYPE_SAME_PIECE:
                same_piece_links.append((u, v, data))
            elif data["edge_type"] == self.LINK_TYPE_INTER_PIECE:
                inter_piece_links.append((u, v, data))

        nx.draw_networkx_edges(self.graph_, pos=pos_spaced, edge_color="black", edgelist=same_piece_links, width=3, ax=ax)
        nx.draw_networkx_edges(self.graph_, pos=pos_spaced, edge_color="blue", edgelist=inter_piece_links, width=3, ax=ax)

    def remove_edges_(self, edges_to_remove: list):
        self.graph_.remove_edges_from(edges_to_remove)
        pos_tmp = nx.shell_layout(self.graph_)
        self.drawing_pos_ = nx.kamada_kawai_layout(self.graph_, pos=pos_tmp, weight="pos_weight")


def get_anchors_from_piece_segmentation(pieces:list[Piece]):
    total_anchors = []

    for piece in pieces:
        segmenting_edges, _ = piece.segment_contour(output_format="edges_tuples")
        anchors = [AnchorConf(edge,piece) for edge in segmenting_edges] 
        total_anchors+= anchors

        # to exploit the 4 permutations of attaching two pieces
        total_anchors+= [anchor.reversed() for anchor in anchors]

    return total_anchors




def anchor_conf_to_matings_(conf1:AnchorConf,conf2:AnchorConf):
    '''
        note - the order of the anchor_points of conf1 and conf2 matters!
    '''
    i = 0
    matings = []
    anchor_points_1 = conf1.get_points()
    anchor_points_2 = conf2.get_points()
    piece_id_1 = conf1.get_parent_piece().get_id()
    piece_id_2 = conf2.get_parent_piece().get_id()

    while i < conf1.get_num_anchors() and i < conf2.get_num_anchors():
        point_1 = anchor_points_1[i]
        point_2 = anchor_points_2[i]
        mating_json = simulator.build_mating_json(piece_id_1,point_1,piece_id_2,point_2)
        matings.append(mating_json)
        i+=1
    
    return matings


def simulate_reconstruction_(anchor_conf_1:AnchorConf,anchor_conf_2:AnchorConf,**params):
    piece_1 = anchor_conf_1.get_parent_piece()
    piece_id_1 = piece_1.get_id()
    piece_2 = anchor_conf_2.get_parent_piece()
    piece_id_2 = piece_2.get_id()
    assert piece_id_1 != piece_id_2

    matings_json = anchor_conf_to_matings_(anchor_conf_1,anchor_conf_2)
    pieces_json = [
        simulator.build_piece_json(piece_id_1,piece_1.get_contour()),
        simulator.build_piece_json(piece_id_2,piece_2.get_contour())
    ]

    return simulator.send_reconstruction(pieces_json,matings_json,**params)

