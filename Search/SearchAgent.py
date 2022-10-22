from Game.ChessState import *


class SearchAgent:

    def __init__(self, depth: int):
        self.depth = depth


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
        state_scores = [self.get_best_action_score(state, new_agent, new_depth)[1] for state in child_states]
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

    def get_action(self, chess_state: ChessState, agent: Color):
        return self.get_best_action_score(chess_state, agent, None, None)[0]

    def get_best_action_score(self, chess_state: ChessState, agent: Color, alpha, beta, depth=0):
        if depth == self.depth or chess_state.is_end_state(agent):
            return None, chess_state.evaluate(agent)

        new_agent = agent.get_opposite()
        new_depth = depth + 1

        legal_actions = chess_state.get_legal_moves(agent)
        val = None
        best_action = None
        for action in legal_actions:
            successor = chess_state.get_successor_state(action, agent)
            successor_score = self.get_best_action_score(successor, new_agent, alpha, beta, new_depth)[1]
            if agent == Color.WHITE:
                if val is None or successor_score > val:
                    val = successor_score
                    best_action = action
                if beta is not None and val > beta:
                    return best_action, val
                if alpha is None or val > alpha:
                    alpha = val
            else:
                if val is None or successor_score < val:
                    val = successor_score
                    best_action = action
                if alpha is not None and val < alpha:
                    return best_action, val
                if beta is None or val < beta:
                    beta = val
        return best_action, val
