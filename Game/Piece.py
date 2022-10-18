from Color import *


class Piece:

    def __init__(self, color: Color):
        self.color = color

    def __eq__(self, other):
        return other == self


class Pawn(Piece):
    def __eq__(self, other):
        return isinstance(other, Pawn) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}P'

    def __hash__(self) -> int:
        return super().__hash__()


class Knight(Piece):
    def __eq__(self, other):
        return isinstance(other, Knight) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}N'

    def __hash__(self) -> int:
        return super().__hash__()


class Bishop(Piece):
    def __eq__(self, other):
        return isinstance(other, Bishop) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}B'

    def __hash__(self) -> int:
        return super().__hash__()


class Rook(Piece):
    def __eq__(self, other):
        return isinstance(other, Rook) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}R'

    def __hash__(self) -> int:
        return super().__hash__()


class Queen(Piece):
    def __eq__(self, other):
        return isinstance(other, Queen) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}Q'

    def __hash__(self) -> int:
        return super().__hash__()


class King(Piece):
    def __eq__(self, other):
        return isinstance(other, King) and other.color == self.color

    def __str__(self) -> str:
        return f'{self.color}K'

    def __hash__(self) -> int:
        return super().__hash__()


class EmptySquare(Piece):

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, EmptySquare)

    def __str__(self) -> str:
        return f'  '

    def __hash__(self) -> int:
        return super().__hash__()


if __name__ == '__main__':
    print(Pawn(Black()))
