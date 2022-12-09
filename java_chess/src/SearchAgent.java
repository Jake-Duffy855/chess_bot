import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class SearchAgent {
  protected final int depth;
  protected final static double GAMMA = 0.99;
  protected int visited = 0;
  protected HashMap<String, Pair<Double, Integer>> visited_states;

  public static void main(String[] args) {
//   args = new String[] {"8/3k1b2/1p4p1/pNp2p1p/PP3P1P/R2p4/1B1n1KP1/4r3 w - - 9 36", "black", "4", "['8/3k1b2/1p4p1/pNp2p1p/PP3P1P/R2p4/1B1n1KP1/4r3 w - - 9 36', '8/3k1b2/1p4p1/pNp2p1p/PP3P1P/R2p4/1B1n1KP1/4r3 w - - 9 36', '8/3k1b2/1p4p1/pNp2p1p/PP3P1P/R2p4/1B1n1KP1/4r3 w - - 9 36']"};
    ChessState c = ChessState.fromFenString(args[0]);
//    System.out.println(c);
    Color agent = Color.fromString(args[1]);
//    System.out.println(c.get_king_pos(agent));
    int depth = Integer.parseInt(args[2]);
    List<String> last_states = last_states_from_string(args[3]);
    c.set_last_states(last_states);
    SearchAgent s = new MultiThreadAgent(depth);
//    System.out.println(c);
//    System.out.println(depth);
//    System.out.println(agent);
    Action a = s.get_action(c, agent);
    System.out.println(a);
    System.out.println(c.evaluate(agent));
    System.out.println(last_states);
//    System.out.println(c);
    c.print_evals();
  }

  public static List<String> last_states_from_string(String states) {
    states = states.replace("['", "");
    states = states.replace("']", "");
    states = states.replace("[", "");
    states = states.replace("]", "");
    states = states.replace(",", "");
    return new ArrayList<>(Arrays.asList(states.split("' '")));
  }

  public SearchAgent(int depth) {
    this.depth = depth;
    this.visited_states  = new HashMap<>();
  }

  public Action get_action(ChessState chessState, Color agent) {
    visited = 0;
    Pair<Action, Double> result = get_best_action_score(chessState, agent, null, null, 0);
//    System.out.println("score: " + result.getSecond());
//    visited_states = new HashMap<>();
    return result.getFirst();
  }

  public Pair<Action, Double> get_best_action_score(ChessState chessState, Color agent, Double alpha, Double beta, int d) {
    String currentFen = chessState.toFenString(agent);
    visited += 1;

    // if seen state before
    if (visited_states.containsKey(currentFen) && d >= visited_states.get(currentFen).getSecond()) {
//      System.out.println(d);
      return new Pair<Action, Double>(null, visited_states.get(currentFen).getFirst());
    }
    // lookup state in saved states {state: (d_val, a, b, score)
    // if d_val <= d: this definitely works
    // ???? if alpha < a or b < beta ???? idk how this works with alpha beta but I'll think about it
    // return score ????


    if (chessState.is_end_state(agent)) {
      int depth_mult = 0;
      if (!chessState.is_draw(agent)) {
        depth_mult = agent == Color.WHITE ? 10 : -10;
      }
      double eval = chessState.evaluate(agent) + d * depth_mult;
      visited_states.put(currentFen, new Pair<>(eval, d));
      return new Pair<Action, Double>(null, eval);
    }
    if (d >= depth) {
      double eval = chessState.evaluate(agent);
      visited_states.put(currentFen, new Pair<>(eval, d));
      return new Pair<Action, Double>(null, eval);
    }

    Color new_agent = agent.get_opposite();
    int new_depth = d + 1;

    List<Action> legal_actions = chessState.get_legal_moves(agent);
    Double val = null;
    Action bestAction = null;
    ChessState bestSuccessor = null;
    for (Action action : legal_actions) {
      ChessState successor = chessState.get_successor_state(action, agent);
      double successor_score = get_best_action_score(successor, new_agent, alpha, beta, new_depth).getSecond();

      if (agent == Color.WHITE) {
        if (val == null || successor_score > val
                || successor_score == val && successor.evaluate(new_agent) > bestSuccessor.evaluate(new_agent)) {
          val = successor_score;
          bestAction = action;
          bestSuccessor = successor;
        }
        if (beta != null && val > beta) {
          visited_states.put(currentFen, new Pair<>(val, d));
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
          visited_states.put(currentFen, new Pair<>(val, d));
          return new Pair<Action, Double>(bestAction, val);
        }
        if (beta == null || val < beta) {
          beta = val;
        }
      }
    }
    visited_states.put(currentFen, new Pair<>(val, d));
    return new Pair<Action, Double>(bestAction, val);
  }
}