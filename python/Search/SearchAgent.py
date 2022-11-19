import sys
import os
from subprocess import Popen, PIPE, STDOUT

path = os.path.dirname(os.path.abspath(__file__))[0:-7]
sys.path.insert(0, path)

from Game.ChessState import *
import time

GAMMA = 0.99


class SearchAgent:

    def __init__(self, depth: int):
        self.depth = depth
        self.memoized_states = {}
        self.num_visited = 0


class MinimaxAgent(SearchAgent):

    def get_action(self, chess_state: ChessState, agent: Color):
        result = self.get_best_action_score(chess_state, agent)[0]
        print(self.num_visited)
        return result

    def get_best_action_score(self, chess_state: ChessState, agent: Color, depth=0) -> tuple[Action, float]:
        self.num_visited += 1
        if depth == self.depth or chess_state.is_end_state(agent):
            return None, chess_state.evaluate(agent)

        new_agent = agent.get_opposite()
        new_depth = depth + 1

        legal_actions = chess_state.get_legal_moves(agent)
        child_states = [chess_state.get_successor_state(action, agent) for action in legal_actions]
        state_scores = [GAMMA ** depth * self.get_best_action_score(state, new_agent, new_depth)[1] for state in
                        child_states]
        if agent == Color.WHITE:
            max_score = max(state_scores)
            max_index = state_scores.index(max_score)
            return legal_actions[max_index], max_score
        else:
            min_score = min(state_scores)
            min_index = state_scores.index(min_score)
            return legal_actions[min_index], min_score


#
class AlphaBetaAgent(SearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, chess_state: ChessState, agent: Color) -> Action:
        self.num_visited = 0
        # self.memoized_states = {}
        a = self.get_best_action_score(chess_state, agent, None, None)
        print(chess_state.__hash__())
        print(a)
        # print((0, chess_state.__hash__()) in self.memoized_states)
        print("-" * 80)
        print(self.num_visited)
        return a[0]

    def get_best_action_score(
            self, chess_state: ChessState, agent: Color, alpha, beta, depth=0) -> tuple[Action, float]:
        self.num_visited += 1
        if depth == self.depth or chess_state.is_end_state(agent):
            return None, chess_state.evaluate(agent)

        # if (depth, agent, alpha, beta, chess_state.__hash__()) in self.memoized_states.keys():
        #     return self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())]

        new_agent = agent.get_opposite()
        new_depth = depth + 1

        legal_actions = chess_state.get_legal_moves(agent)
        val = None
        best_action = None
        for action in legal_actions:
            successor = chess_state.get_successor_state(action, agent)
            successor_score = self.get_best_action_score(successor, new_agent, alpha, beta, new_depth)[1]
            if agent == Color.WHITE and successor_score == 1000 or agent == Color.BLACK and successor_score == -1000:
                self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = action, successor_score
                return action, successor_score
            successor_score = GAMMA ** depth * successor_score
            if agent == Color.WHITE:
                if val is None or successor_score > val:  # or successor_score == val and successor.evaluate(agent) > chess_state.evaluate(agent):
                    # could be good ^^^^ but slow evaluate
                    val = successor_score
                    best_action = action
                if beta is not None and val > beta:
                    self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
                    return best_action, val
                if alpha is None or val > alpha:
                    alpha = val
            else:
                if val is None or successor_score < val:  # or successor_score == val and successor.evaluate(agent) < chess_state.evaluate(agent):
                    val = successor_score
                    best_action = action
                if alpha is not None and val < alpha:
                    self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
                    return best_action, val
                if beta is None or val < beta:
                    beta = val

        self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
        return best_action, val


class JavaSearchAgent(SearchAgent):

    def get_action(self, chess_state: ChessState, agent: Color) -> Action:
        # call jar with state rep as args
        # print(str(agent))
        p = Popen(
            ['java', '-jar', '/Users/jakeduffy/Documents/CS4100/java_chess/out/artifacts/get_action/get_action.jar',
             str(chess_state),
             agent.get_string(), str(self.depth)], stdout=PIPE, stderr=STDOUT)
        print(str(chess_state))
        for line in p.stdout:
            print(line.decode('utf-8'))
            return Action.from_string(line.decode('utf-8'))


if __name__ == '__main__':
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        c = ChessState(DEFAULT_BOARD)
        print(c)
        search_agent = JavaSearchAgent(depth=4)
        agent = Color.WHITE
        for i in range(50):
            best_move = search_agent.get_action(c, agent)
            c = c.get_successor_state(best_move, agent)
            print(best_move)
            print(c)
            agent = agent.get_opposite()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
