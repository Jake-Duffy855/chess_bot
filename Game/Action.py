from Piece import *


class Action:

    def __init__(self, start_piece: Piece, end_piece: Piece):
        self.start_piece = start_piece
        self.end_piece = end_piece

    def get_start_pos(self):
        return self.start_piece.pos

    def get_end_pos(self):
        return self.end_piece.pos
