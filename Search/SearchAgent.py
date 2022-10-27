from Game.ChessState import *
import time

GAMMA = 0.99


class SearchAgent:

    def __init__(self, depth: int):
        self.depth = depth
        self.memoized_states = {}


class MinimaxAgent(SearchAgent):

    def get_action(self, chess_state: ChessState, agent: Color):
        return self.get_best_action_score(chess_state, agent)[0]

    def get_best_action_score(self, chess_state: ChessState, agent: Color, depth=0) -> tuple[Action, float]:
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
        # self.memoized_states = {}
        a = self.get_best_action_score(chess_state, agent, None, None)
        print(chess_state.__hash__())
        print(a)
        # print((0, chess_state.__hash__()) in self.memoized_states)
        print("-"*80)
        return a[0]

    def get_best_action_score(
            self, chess_state: ChessState, agent: Color, alpha, beta, depth=0) -> tuple[Action, float]:
        if depth == self.depth or chess_state.is_end_state(agent):
            return None, chess_state.evaluate(agent)

        # figure out hashing and this should help??? THis should help if I can figure it out but my brain is broken
        # print(self.memoized_states.keys())
        # not working, repeat states aren't going insanely fast!!!!!!
        if (depth, agent, alpha, beta, chess_state.__hash__()) in self.memoized_states.keys():
            # print((depth, agent, chess_state.__hash__()))
            return self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())]

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
                if val is None or successor_score > val: # or successor_score == val and successor.evaluate(agent) > chess_state.evaluate(agent):
                    # could be good ^^^^ but slow evaluate
                    val = successor_score
                    best_action = action
                if beta is not None and val > beta:
                    self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
                    return best_action, val
                if alpha is None or val > alpha:
                    alpha = val
            else:
                if val is None or successor_score < val: # or successor_score == val and successor.evaluate(agent) < chess_state.evaluate(agent):
                    val = successor_score
                    best_action = action
                if alpha is not None and val < alpha:
                    self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
                    return best_action, val
                if beta is None or val < beta:
                    beta = val

        self.memoized_states[(depth, agent, alpha, beta, chess_state.__hash__())] = best_action, val
        return best_action, val


# class TimedAlphaBetaAgent(SearchAgent):
#
#     def __init__(self, depth: int, max_time: float):
#         self.depth = depth
#         self.max_time = max_time
#
#
#     def get_action(self, chess_state: ChessState, agent: Color) -> Action:
#         start_time = time.time()
#         a = self.get_best_action_score(chess_state, agent, None, None, start_time, depth=0)
#         print(a)
#         return a[0]
#
#     def get_best_action_score(self, chess_state: ChessState, agent: Color, alpha, beta,
#                               start_time, depth=0) -> tuple[Action, float]:
#         if depth == self.depth or self.max_time < (time.time() - start_time) or chess_state.is_end_state(agent):
#             return Action((-1, -1), (-1, -1)), chess_state.evaluate(agent)
#
#         new_agent = agent.get_opposite()
#         new_depth = depth + 1
#
#         legal_actions = chess_state.get_legal_moves(agent)
#         val = None
#         best_action = None
#         for action in legal_actions:
#             successor = chess_state.get_successor_state(action, agent)
#             successor_score = self.get_best_action_score(successor, new_agent, alpha, beta, start_time, new_depth)[1]
#             if agent == Color.WHITE:
#                 if val is None or successor_score > val:
#                     val = successor_score
#                     best_action = action
#                 if beta is not None and val > beta:
#                     return best_action, val
#                 if alpha is None or val > alpha:
#                     alpha = val
#             else:
#                 if val is None or successor_score < val:
#                     val = successor_score
#                     best_action = action
#                 if alpha is not None and val < alpha:
#                     return best_action, val
#                 if beta is None or val < beta:
#                     beta = val
#         return best_action, val


if __name__ == '__main__':
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        c = ChessState(SMALL_GAME)
        search_agent = AlphaBetaAgent(depth=8)
        best_move = search_agent.get_action(c, Color.WHITE)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
