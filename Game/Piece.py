from Color import *
from Action import *


class Piece:

    def __init__(self, color: Color):
        self.color = color

    def __eq__(self, other):
        return self is other

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        pass


class Pawn(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        if self.color == Black():
            step = 1
            double = [Action(loc, (i + 2 * step, j))] if i == 1 else []
        else:
            step = -1
            double = [Action(loc, (i + 2 * step, j))] if i == 6 else []
        return [Action(loc, (i + step, j)), Action(loc, (i + step, j + 1)), Action(loc, (i + step, j - 1))] + double

    def __eq__(self, other):
        return self is other or isinstance(other, Pawn) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♙'
        return '♟'

    def __hash__(self) -> int:
        return super().__hash__()


class Knight(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        return [Action(loc, (i + di, j + dj)) for di, dj in diffs]

    def __eq__(self, other):
        return self is other or isinstance(other, Knight) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♘'
        return '♞'

    def __hash__(self) -> int:
        return super().__hash__()


class Bishop(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
        return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs]

    def __eq__(self, other):
        return self is other or isinstance(other, Bishop) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♗'
        return '♝'

    def __hash__(self) -> int:
        return super().__hash__()


class Rook(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
        return [Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]

    def __eq__(self, other):
        return self is other or isinstance(other, Rook) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♖'
        return '♜'

    def __hash__(self) -> int:
        return super().__hash__()


class Queen(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
        return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs] + [
            Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]

    def __eq__(self, other):
        return self is other or isinstance(other, Queen) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♕'
        return '♛'

    def __hash__(self) -> int:
        return super().__hash__()


class King(Piece):

    def __init__(self, color: Color):
        self.color = color

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        i, j = loc
        return [Action(loc, (i + di, j + dj)) for di in range(-1, 2) for dj in range(-1, 2) if di != 0 or dj != 0]

    def __eq__(self, other):
        return self is other or isinstance(other, King) and other.color == self.color

    def __str__(self) -> str:
        if self.color == White():
            return '♔'
        return '♚'

    def __hash__(self) -> int:
        return super().__hash__()


class EmptySquare(Piece):

    def __init__(self):
        pass

    def get_possible_moves_from(self, loc: tuple[int, int], board_size=(8, 8)) -> list[Action]:
        return []

    def __eq__(self, other):
        return self is other or isinstance(other, EmptySquare)

    def __str__(self) -> str:
        return f' '

    def __hash__(self) -> int:
        return super().__hash__()


if __name__ == '__main__':
    print([str(a) for a in Rook(White()).get_possible_moves_from((6, 4))])
