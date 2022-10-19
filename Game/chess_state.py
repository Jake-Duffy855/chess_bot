from Action import Action
from Piece import *
from Color import *
import random

DEFAULT_BOARD = [
    [Rook(Black()), Knight(Black()), Bishop(Black()), Queen(Black()),
     King(Black()), Bishop(Black()), Knight(Black()), Rook(Black())],
    [Pawn(Black()) for _ in range(8)],
    [EmptySquare() for _ in range(8)],
    [EmptySquare() for _ in range(8)],
    [EmptySquare() for _ in range(8)],
    [EmptySquare() for _ in range(8)],
    [Pawn(White()) for _ in range(8)],
    [Rook(White()), Knight(White()), Bishop(White()), Queen(White()),
     King(White()), Bishop(White()), Knight(White()), Rook(White())]
]


class ChessState:

    def __init__(self, pieces: list[list[Piece]], wcl=True, wcr=True, bcl=True, bcr=True, en_passant=()):
        self.pieces = pieces
        self.size = (len(pieces), len(pieces[0]))
        self.wcl = wcl
        self.wcr = wcr
        self.bcl = bcl
        self.bcr = bcr
        self.en_passant = en_passant

    def get_legal_moves(self, agent: Color) -> list[Action]:
        legal_moves = []
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                legal_moves.extend(
                    [action for action in piece.get_possible_moves_from((i, j)) if self.__is_legal_move(action, agent)]
                )
        return legal_moves

    def get_successor_state(self, action: Action, agent: Color):
        if self.__is_legal_move(action, agent):
            new_pieces = [[piece for piece in row] for row in self.pieces]
            sx, sy = action.start_pos
            ex, ey = action.end_pos
            new_pieces[ex][ey] = self.get_piece_at(action.start_pos)
            new_pieces[sx][sy] = EmptySquare()

            return ChessState(new_pieces)
        else:
            raise ValueError("Bruh")

    def __is_legal_move(self, action: Action, agent: Color) -> bool:
        sloc = action.start_pos
        eloc = action.end_pos
        # moving piece off of board
        if min(sloc + eloc) < 0 or max(sloc[0], eloc[0]) >= self.size[0] or max(sloc[1], eloc[1]) >= self.size[1]:
            return False
        # moving wrong color piece or empty square
        if self.get_piece_at(sloc) == EmptySquare() or self.get_piece_at(sloc).color != agent:
            return False
        # moving piece onto own piece
        if self.get_piece_at(eloc) != EmptySquare() and self.get_piece_at(eloc).color == agent:
            return False

        if self.get_piece_at(sloc) == Pawn(agent):
            pass
        elif self.get_piece_at(sloc) == Knight(agent):
            pass

        return True

    def get_piece_at(self, loc: tuple[int, int]) -> Piece:
        return self.pieces[loc[0]][loc[1]]

    def evaluate(self) -> float:
        return 0

    def __str__(self) -> str:
        result = "-" * 41 + "\n"
        for row in self.pieces:
            for piece in row:
                result += "| " + str(piece) + " "
            result += "|\n" + "-" * 41 + "\n"
        return result


if __name__ == '__main__':
    c = ChessState(DEFAULT_BOARD)
    idx = 0
    while idx < 100:
        print(c)
        if idx % 2 == 0:
            a = White()
        else:
            a = Black()
        c = c.get_successor_state(random.choice(c.get_legal_moves(a)), a)
        idx += 1
        input()

