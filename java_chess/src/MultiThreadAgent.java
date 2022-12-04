import java.util.ArrayList;
import java.util.List;
import java.lang.*;


public class MultiThreadAgent extends SearchAgent{
  private int MAX_THREADS;

  public MultiThreadAgent(int depth) {
    this(depth, 4);
  }

  public MultiThreadAgent(int depth, int threads) {
    super(depth);
    MAX_THREADS = threads;
  }

  private class MultiThreads implements Runnable {

    ChessState state;
    Color agent;
    int depth;
    volatile Pair<Action, Double> result;

    public MultiThreads(ChessState state, Color agent, int depth) {
      this.state = state;
      this.agent = agent;
      this.depth = depth;
    }

    @Override
    public void run() {
      this.result = get_best_action_score(this.state, agent, null, null, this.depth);
    }

    public Pair<Action, Double> getResult() {
      return this.result;
    }

  }

  @Override
  public Action get_action(ChessState chessState, Color agent) {
    // maintain order of arrays please!!!!!!!!
    int startDepth = 1;
    Action bestAction = null;
    visited = 0;
    while (visited < 10000 && startDepth > -4) {
      long start_time = System.currentTimeMillis();
      visited = 0;
      List<Action> legal_moves = chessState.get_legal_moves(agent);
      List<MultiThreads> m_threads = new ArrayList<>();
      List<Thread> threads = new ArrayList<>();

      List<Pair<Action, Double>> results = new ArrayList<>();

      for (Action move : legal_moves) {
        // start thread
        MultiThreads m = new MultiThreads(chessState.get_successor_state(move, agent), agent.get_opposite(), startDepth);
        Thread t = new Thread(m);
        t.start();
        m_threads.add(m);
        threads.add(t);
      }

      for (int i = 0; i < threads.size(); i++) {
        try {
          threads.get(i).join();
        } catch (InterruptedException e) {
          e.printStackTrace();
        }
      }

      for (int i = 0; i < m_threads.size(); i++) {
        results.add(m_threads.get(i).getResult());
      }

      bestAction = null;
      double bestScore = 0;
      for (int i = 0; i < results.size(); i++) {
        Pair<Action, Double> p = results.get(i);
        if (bestAction == null) {
          bestAction = legal_moves.get(i);
          bestScore = p.getSecond();
        }
        if (agent == Color.WHITE && p.getSecond() > bestScore
                || agent == Color.BLACK && p.getSecond() < bestScore) {
          bestAction = legal_moves.get(i);
          bestScore = p.getSecond();
        }
      }
//      System.out.println("Visited: " + visited);
//      System.out.println("Time: " + (System.currentTimeMillis() - start_time));
//      System.out.println("Start depth: " + startDepth);
      startDepth -= 1;
    }
    return bestAction;
  }

}
