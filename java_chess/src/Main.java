import java.util.ArrayList;
import java.util.List;

public class Main {
  public static void main(String[] args) {
    Color agent = Color.WHITE;
    ChessState c = new ChessState();
    SearchAgent s = new MultiThreadAgent(4);
    System.out.println(c);
    for (int i = 0; i < 5; i++) {
      c = c.get_successor_state(s.get_action(c, agent), agent);
      System.out.println(c);
      agent = agent.get_opposite();
    }
  }
}
