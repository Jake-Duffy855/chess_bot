from Action import Action
from Piece import *
from Color import *

DEFAULT_BOARD = [
    [Rook((0, 0), Black()), Knight((0, 1), Black()), Bishop((0, 2), Black()), Queen((0, 3), Black()),
     King((0, 4), Black()), Bishop((0, 5), Black()), Knight((0, 6), Black()), Rook((0, 7), Black())],
    [Pawn((1, i), Black()) for i in range(8)],
    [EmptySquare((2, i)) for i in range(8)],
    [EmptySquare((3, i)) for i in range(8)],
    [EmptySquare((4, i)) for i in range(8)],
    [EmptySquare((5, i)) for i in range(8)],
    [Pawn((6, i), White()) for i in range(8)],
    [Rook((7, 0), White()), Knight((7, 1), White()), Bishop((7, 2), White()), Queen((7, 3), White()),
     King((7, 4), White()), Bishop((7, 5), White()), Knight((7, 6), White()), Rook((7, 7), White())]
]


class ChessState:

    def __init__(self, pieces):
        self.pieces = pieces
        self.size = (len(pieces), len(pieces[0]))

    def get_legal_moves(self, agent):
        return None

    def get_successor_state(self, action: Action, agent: Color):
        new_pieces = [[piece for piece in row] for row in self.pieces]
        x, y = action.get_start_pos()
        new_pieces[x][y] = EmptySquare(action.get_start_pos())
        x, y = action.get_end_pos()
        new_pieces[x][y] = action.end_piece

        return ChessState(new_pieces)


    def __str__(self):
        result = "-" * 41 + "\n"
        for row in self.pieces:
            for piece in row:
                result += "| " + str(piece) + " "
            result += "|\n" + "-" * 41 + "\n"
        return result


if __name__ == '__main__':
    c = ChessState(DEFAULT_BOARD)
    print(c)
    print(c.get_successor_state(Action(DEFAULT_BOARD[6][4], Pawn((4, 4), White())), White()))
