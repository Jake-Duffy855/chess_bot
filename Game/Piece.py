from Color import *
from Action import *

from enum import Enum

STRING_REPS = ['♙', '♘', '♗', '♖', '♕', '♔', '♟', '♞', '♝', '♜', '♛', '♚', " "]


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

    def __str__(self):
        return STRING_REPS[self.value]

    def get_possible_moves_from(self, loc):
        i, j = loc
        if self.is_pawn():
            if self.is_black():
                step = 1
                double = [Action(loc, (i + 2 * step, j))] if i == 1 else []
            else:
                step = -1
                double = [Action(loc, (i + 2 * step, j))] if i == 6 else []
            return [Action(loc, (i + step, j)), Action(loc, (i + step, j + 1)), Action(loc, (i + step, j - 1))] + double
        elif self.is_knight():
            diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
            return [Action(loc, (i + di, j + dj)) for di, dj in diffs]
        elif self.is_bishop():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs]
        elif self.is_rook():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
        elif self.is_queen():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs] + [
                Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
        elif self.is_king():
            return [Action(loc, (i + di, j + dj)) for di in range(-1, 2) for dj in range(-1, 2) if di != 0 or dj != 0]
        return []

#
# class Pawn(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         if self.color == Color.BLACK:
#             step = 1
#             double = [Action(loc, (i + 2 * step, j))] if i == 1 else []
#         else:
#             step = -1
#             double = [Action(loc, (i + 2 * step, j))] if i == 6 else []
#         return [Action(loc, (i + step, j)), Action(loc, (i + step, j + 1)), Action(loc, (i + step, j - 1))] + double
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, Pawn) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♙'
#         return '♟'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class Knight(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
#         return [Action(loc, (i + di, j + dj)) for di, dj in diffs]
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, Knight) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♘'
#         return '♞'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class Bishop(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
#         return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs]
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, Bishop) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♗'
#         return '♝'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class Rook(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
#         return [Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, Rook) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♖'
#         return '♜'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class Queen(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
#         return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs] + [
#             Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, Queen) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♕'
#         return '♛'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class King(Piece):
#
#     def __init__(self, color: Color):
#         self.color = color
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         i, j = loc
#         return [Action(loc, (i + di, j + dj)) for di in range(-1, 2) for dj in range(-1, 2) if di != 0 or dj != 0]
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, King) and other.color == self.color
#
#     def __str__(self) -> str:
#         if self.color == Color.WHITE:
#             return '♔'
#         return '♚'
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
# class EmptySquare(Piece):
#
#     def __init__(self):
#         pass
#
#     def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
#         return []
#
#     def __eq__(self, other):
#         return self is other or isinstance(other, EmptySquare)
#
#     def __str__(self) -> str:
#         return f' '
#
#     def __hash__(self) -> int:
#         return super().__hash__()
#
#
if __name__ == '__main__':
    print(Piece.BLACK_ROOK.is_color(Color.BLACK))
