from src.piece import Piece
from functools import reduce

class AnchorConf():

    def __init__(self,anchor_points:list,parent_piece:Piece,**metadata) -> None:
        '''
            anchor_points - list of tuples of numbers  - the order in the list matters! (it determines the permutation)
            parent_piece - piece to be anchored
        '''
        assert isinstance(anchor_points,list)
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
