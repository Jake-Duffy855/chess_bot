from Color import *


class Piece:

    def __init__(self, pos: tuple, color: Color):
        self.pos = pos
        self.color = color

    def __eq__(self, other):
        return other == self


class Pawn(Piece):
    def __eq__(self, other):
        return other is Pawn and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}P'

    def __hash__(self) -> int:
        return super().__hash__()


class Knight(Piece):
    def __eq__(self, other):
        return other is Knight and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}N'

    def __hash__(self) -> int:
        return super().__hash__()


class Bishop(Piece):
    def __eq__(self, other):
        return other is Bishop and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}B'

    def __hash__(self) -> int:
        return super().__hash__()


class Rook(Piece):
    def __eq__(self, other):
        return other is Rook and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}R'

    def __hash__(self) -> int:
        return super().__hash__()


class Queen(Piece):
    def __eq__(self, other):
        return other is Queen and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}Q'

    def __hash__(self) -> int:
        return super().__hash__()


class King(Piece):
    def __eq__(self, other):
        return other is King and other.color == self.color and other.pos == self.pos

    def __str__(self) -> str:
        return f'{self.color}K'

    def __hash__(self) -> int:
        return super().__hash__()


class EmptySquare(Piece):

    def __init__(self, loc):
        self.loc = loc

    def __eq__(self, other):
        return other is EmptySquare and other.pos == self.pos

    def __str__(self) -> str:
        return f'  '

    def __hash__(self) -> int:
        return super().__hash__()


if __name__ == '__main__':
    print(Pawn((1, 1), Black()))
