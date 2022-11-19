import java.util.List;

public class MultiThreadAgent extends SearchAgent{
  private int MAX_THREADS;

  public MultiThreadAgent(int depth) {
    this(depth, 4);
  }

  public MultiThreadAgent(int depth, int threads) {
    super(depth);
    MAX_THREADS = threads;
  }

  @Override
  public Action get_action(ChessState chessState, Color agent) {
    visited = 0;
    List<Action> legal_moves = chessState.get_legal_moves(agent);

    for (Action move : legal_moves) {
      // start thread
      // Pair<Action, Double> result = get_best_action_score(chessState.get_successor_state(move, agent), agent, null, null, 0);
    }
    System.out.println(visited);
    return result.getFirst();
  }

}
