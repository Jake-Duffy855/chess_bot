import ChessState
from Game import Action
from Game.Color import Color
from Game.Piece import Piece


class JavaChessState(ChessState):

    def get_legal_moves(self, agent: Color) -> list[Action]:
        pass

    def get_possible_moves(self, piece: Piece, loc, agent: Color):
        pass

    def get_successor_state(self, action: Action, agent: Color):
        pass

    def is_legal_move(self, action: Action, agent: Color) -> bool:
        pass

    def is_in_check(self, new_pieces: list[list[Piece]], agent: Color, king_pos) -> bool:
        pass

    def is_win(self):
        pass

    def is_lose(self):
        pass

    def is_draw(self):
        pass

    def is_stalemate(self):
        pass

    def is_end_state(self, agent):
        return not self.get_legal_moves(agent)

    def get_piece_at(self, loc: tuple[int, int]) -> Piece:
        return self.pieces[loc[0]][loc[1]]

    def evaluate(self, agent) -> float:
        pass

    def __str__(self) -> str:
        result = "-" * 23 + "\n"
        for row in self.pieces:
            for piece in row:
                result += str(piece) + "  "
            result += "\n"
        result += "-" * 23
        return result

    def __hash__(self) -> int:
        return self.__str__().__hash__()

