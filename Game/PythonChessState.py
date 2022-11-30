from Game.ChessState import *
from Game.Action import *
from Game.Color import Color
from Game.Piece import Piece
from subprocess import Popen, PIPE, STDOUT
import chess


class PythonChessState(ChessState):

    def get_legal_moves(self, agent: Color) -> list[Action]:
        # print(5)
        return [PythonChessState.chess_move_to_action(m) for m in
                chess.Board(self.to_fen().replace("to_move", agent.get_fen())).legal_moves]

    @staticmethod
    def chess_move_to_action(move):
        str_move = chess.Move.uci(move)
        from_pos = (8 - int(str_move[1]), ord(str_move[0]) - 97)
        to_pos = (8 - int(str_move[3]), ord(str_move[2]) - 97)
        return Action(from_pos, to_pos)

    # def is_legal_move(self, action: Action, agent: Color) -> bool:
    #     return False

    def get_successor_state(self, action: Action, agent: Color):
        new_pieces = self._ChessState__move_loc_to_loc(action.start_pos, action.end_pos)
        # castle: move rook, still need to add checks for moved kings and moved rooks and moving through check
        spiece = self.pieces[action.start_pos[0]][action.start_pos[1]]
        new_white_king_pos = self.white_king_pos
        new_black_king_pos = self.black_king_pos
        new_wcl, new_wcr, new_bcl, new_bcr = self.wcl, self.wcr, self.bcl, self.bcr
        if spiece.is_king():
            new_wcl, new_wcr, new_bcl, new_bcr = self._ChessState__update_castling(action)
            if spiece.is_white():
                new_white_king_pos = action.end_pos
            else:
                new_black_king_pos = action.end_pos
        if spiece.is_rook():
            new_wcl, new_wcr, new_bcl, new_bcr = self._ChessState__update_castling(action)

        return PythonChessState(new_pieces, new_wcl, new_wcr, new_bcl, new_bcr,
                                white_king_pos=new_white_king_pos,
                                black_king_pos=new_black_king_pos)


if __name__ == '__main__':
    # b = chess.Board()
    # for m in b.legal_moves:
    #     print(chess.Move.uci(m))
    # print(b)
    # print(b.legal_moves)
    c = PythonChessState(DEFAULT_BOARD)
    print([chess.Move.uci(move) for move in chess.Board().legal_moves])
    print([str(PythonChessState.chess_move_to_action(move)) for move in chess.Board().legal_moves])
