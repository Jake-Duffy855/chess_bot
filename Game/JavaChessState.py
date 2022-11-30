from Game.ChessState import *
from Game.Action import *
from Game.Color import Color
from Game.Piece import Piece
from subprocess import Popen, PIPE, STDOUT


class JavaChessState(ChessState):

    def get_legal_moves(self, agent: Color) -> list[Action]:
        p = Popen(
            ['java', '-jar',
             '/Users/jakeduffy/Documents/CS4100/chess_bot/java_chess/out/artifacts/get_legal_moves/get_legal_moves.jar',
             str(self), agent.get_string()], stdout=PIPE, stderr=STDOUT)
        # print(str(self))
        for line in p.stdout:
            line = line.decode('utf-8')
            line = line[1:-1]
            # print(line)
            return [Action.from_string(action_string) for action_string in line.split("), ")]
            # return Action.from_string(line.decode('utf-8'))

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

        return JavaChessState(new_pieces, new_wcl, new_wcr, new_bcl, new_bcr,
                              white_king_pos=new_white_king_pos,
                              black_king_pos=new_black_king_pos)


if __name__ == '__main__':
    j = JavaChessState(DEFAULT_BOARD)
    print(j.get_legal_moves(Color.WHITE))
