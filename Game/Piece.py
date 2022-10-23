from Game.Color import *
from Game.Action import *

from enum import Enum

STRING_REPS = ['♙', '♘', '♗', '♖', '♕', '♔', '♟', '♞', '♝', '♜', '♛', '♚', " "]
MATERIAL_VALUE = [1, 3, 3, 5, 9, 0, -1, -3, -3, -5, -9, 0, 0]
SLIDING_NUMBERS = {2, 3, 4}


class Piece(Enum):
    WHITE_PAWN = 0
    WHITE_KNIGHT = 1
    WHITE_BISHOP = 2
    WHITE_ROOK = 3
    WHITE_QUEEN = 4
    WHITE_KING = 5

    BLACK_PAWN = 6
    BLACK_KNIGHT = 7
    BLACK_BISHOP = 8
    BLACK_ROOK = 9
    BLACK_QUEEN = 10
    BLACK_KING = 11

    EMPTY = 12

    def get_color(self):
        if self.is_empty():
            raise ValueError("Blank doesn't have color")
        return Color.WHITE if self.value < 6 else Color.BLACK

    def is_white(self):
        return self.value < 6

    def is_black(self):
        return 12 > self.value >= 6

    def is_color(self, color: Color):
        if color == Color.WHITE:
            return self.value < 6
        return 12 > self.value >= 6

    def get_value(self):
        return MATERIAL_VALUE[self.value]

    def is_pawn(self):
        return self.value % 6 == 0 and self.value != 12

    def is_knight(self):
        return self.value % 6 == 1

    def is_bishop(self):
        return self.value % 6 == 2

    def is_rook(self):
        return self.value % 6 == 3

    def is_queen(self):
        return self.value % 6 == 4

    def is_king(self):
        return self.value % 6 == 5

    def is_empty(self):
        return self.value == 12

    def is_sliding(self):
        return self.value % 6 in SLIDING_NUMBERS

    def __str__(self):
        return STRING_REPS[self.value]


if __name__ == '__main__':
    print([str(m) for m in Piece.WHITE_KING.get_possible_moves_from((4, 4))])
