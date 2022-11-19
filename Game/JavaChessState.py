from Game.ChessState import *
from Game.Action import *
from Game.Color import Color
from Game.Piece import Piece
from subprocess import Popen, PIPE, STDOUT


class JavaChessState(ChessState):

    def get_legal_moves(self, agent: Color) -> list[Action]:
        p = Popen(
            ['java', '-jar', '/Users/jakeduffy/Documents/CS4100/chess_bot/java_chess/out/artifacts/get_legal_moves/get_legal_moves.jar',
             str(self), agent.get_string()], stdout=PIPE, stderr=STDOUT)
        # print(str(self))
        for line in p.stdout:
            line = line.decode('utf-8')
            line = line[1:-1]
            # print(line)
            return [Action.from_string(action_string) for action_string in line.split("), ")]
            # return Action.from_string(line.decode('utf-8'))


if __name__ == '__main__':
    j = JavaChessState(DEFAULT_BOARD)
    print(j.get_legal_moves(Color.WHITE))




