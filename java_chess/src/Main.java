import java.util.ArrayList;
import java.util.List;

public class Main {
  public static void main(String[] args) {
    Color agent = Color.WHITE;
    ChessState c =ChessState.fromFenString("4k3/8/8/8/8/8/2P5/4K3 w KQkq - 0 1");
    SearchAgent s = new MultiThreadAgent(4);
    while (!c.is_end_state(agent)) {
      System.out.println(c);
      Action move = s.get_action(c, agent);
      c = c.get_successor_state(move, agent);
      System.out.println(move);
      System.out.println(c.evaluate(agent));
      c.print_evals();
      agent = agent.get_opposite();
    }
    System.out.println(c);
    System.out.println(c.evaluate(agent));
    c.print_evals();
    agent = agent.get_opposite();
  }
}
