import java.util.List;

public class SearchAgent {
  protected final int depth;
  protected final static double GAMMA = 0.99;
  protected int visited = 0;

  public static void main(String[] args) {
//   args = new String[] {"-----------------------\n" +
//           "                     ♜  \n" +
//           "♜  ♟  ♟  ♚  ♞  ♗        \n" +
//           "         ♛     ♟        \n" +
//           "♟     ♟     ♟     ♟     \n" +
//           "♙           ♙        ♟  \n" +
//           "   ♕     ♙     ♘     ♙  \n" +
//           "   ♙           ♙  ♙     \n" +
//           "   ♖     ♖        ♔     \n" +
//           "-----------------------", "black", "5"};
    ChessState c = ChessState.fromString(args[0]);
    Color agent = Color.fromString(args[1]);
//    System.out.println(c.get_king_pos(agent));
    int depth = Integer.parseInt(args[2]);
    SearchAgent s = new MultiThreadAgent(depth);
//    System.out.println(c);
//    System.out.println(depth);
//    System.out.println(agent);
    Action a = s.get_action(c, agent);
    System.out.println(a);
    System.out.println(c.evaluate(agent));
    c.print_evals();
  }

  public SearchAgent(int depth) {
    this.depth = depth;
  }

  public Action get_action(ChessState chessState, Color agent) {
    visited = 0;
    Pair<Action, Double> result = get_best_action_score(chessState, agent, null, null, 0);
//    System.out.println(visited);
    return result.getFirst();
  }

  public Pair<Action, Double> get_best_action_score(ChessState chessState, Color agent, Double alpha, Double beta, int d) {
    visited += 1;
    if (d >= depth || chessState.is_end_state(agent)) {
      return new Pair<Action, Double>(null, chessState.evaluate(agent));
    }
    Color new_agent = agent.get_opposite();
    int new_depth = d + 1;

    List<Action> legal_actions = chessState.get_legal_moves(agent);
    Double val = null;
    Action bestAction = null;
    for (Action action : legal_actions) {
      ChessState successor = chessState.get_successor_state(action, agent);
      double successor_score = get_best_action_score(successor, new_agent, alpha, beta, new_depth).getSecond();
      if (agent == Color.WHITE && successor_score == 1000 || agent == Color.BLACK && successor_score == -1000) {
        return new Pair<>(action, successor_score);
      }
      successor_score = Math.pow(GAMMA, depth) * successor_score;

      if (agent == Color.WHITE) {
        if (val == null || successor_score > val) {
          val = successor_score;
          bestAction = action;
        }
        if (beta != null && val > beta) {
          return new Pair<Action, Double>(bestAction, val);
        }
        if (alpha == null || val > alpha) {
          alpha = val;
        }
      } else{
        if (val == null || successor_score < val) {
          val = successor_score;
          bestAction = action;
        }
        if (alpha != null && val < alpha) {
          return new Pair<Action, Double>(bestAction, val);
        }
        if (beta == null || val < beta) {
          beta = val;
        }
      }
    }
    return new Pair<Action, Double>(bestAction, val);
  }
}