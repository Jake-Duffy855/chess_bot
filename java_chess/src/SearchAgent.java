import java.util.List;

public class SearchAgent {
  protected final int depth;
  protected final static double GAMMA = 0.99;
  protected int visited = 0;
  protected String startStateFen;

  public static void main(String[] args) {
   args = new String[] {"8/3k1b2/1p4p1/pNp2p1p/PP3P1P/R2p4/1B1n1KP1/4r3 w - - 9 36", "black", "4"};
    ChessState c = ChessState.fromFenString(args[0]);
    System.out.println(c);
    Color agent = Color.fromString(args[1]);
//    System.out.println(c.get_king_pos(agent));
    int depth = Integer.parseInt(args[2]);
    SearchAgent s = new MultiThreadAgent(depth);
//    System.out.println(c);
//    System.out.println(depth);
//    System.out.println(agent);
    Action a = s.get_action(c, agent);
    System.out.println(a);
    System.out.println(" bar" +c.evaluate(agent));
//    System.out.println(c);
    c.print_evals();
  }

  public SearchAgent(int depth) {
    this.depth = depth;
  }

  public Action get_action(ChessState chessState, Color agent) {
    visited = 0;
    startStateFen = chessState.toFenString(agent);
    Pair<Action, Double> result = get_best_action_score(chessState, agent, null, null, 0);
    startStateFen = null;
    return result.getFirst();
  }

  public Pair<Action, Double> get_best_action_score(ChessState chessState, Color agent, Double alpha, Double beta, int d) {
    visited += 1;

    if (chessState.is_end_state(agent)) {
      int depth_mult = 0;
      if (!chessState.is_draw()) {
        depth_mult = agent == Color.WHITE ? 10 : -10;
      }
      return new Pair<Action, Double>(null, chessState.evaluate(agent) + d * depth_mult);
    }
    if (d >= depth) {
      return new Pair<Action, Double>(null, chessState.evaluate(agent));
    }

    Color new_agent = agent.get_opposite();
    int new_depth = d + 1;

    List<Action> legal_actions = chessState.get_legal_moves(agent);
    Double val = null;
    Action bestAction = null;
    ChessState bestSuccessor = null;
    for (Action action : legal_actions) {
      ChessState successor = chessState.get_successor_state(action, agent);
      double successor_score;
      if (successor.toFenString(new_agent).equals(startStateFen)) {
        successor_score = 0;
        System.out.println("" +action + d);
      } else {
        successor_score = get_best_action_score(successor, new_agent, alpha, beta, new_depth).getSecond();
      }

      if (agent == Color.WHITE) {
        if (val == null || successor_score > val
                || successor_score == val && successor.evaluate(new_agent) > bestSuccessor.evaluate(new_agent)) {
          val = successor_score;
          bestAction = action;
          bestSuccessor = successor;
        }
        if (beta != null && val > beta) {
          return new Pair<Action, Double>(bestAction, val);
        }
        if (alpha == null || val > alpha) {
          alpha = val;
        }
      } else{
        if (val == null || successor_score < val
                || successor_score == val && successor.evaluate(new_agent) < bestSuccessor.evaluate(new_agent)) {
          val = successor_score;
          bestAction = action;
          bestSuccessor = successor;
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