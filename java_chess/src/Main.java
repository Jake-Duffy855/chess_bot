import java.util.List;

public class Main {
  public static void main(String[] args) {
    Color agent = Color.WHITE;
    ChessState c = new ChessState();
    SearchAgent s = new SearchAgent(5);
    System.out.println(c);
    for (int i = 0; i < 50; i++) {
      List<Action> m = c.get_legal_moves(agent);
      Action a = s.get_action(c, agent);
      c = c.get_successor_state(a, agent);
      System.out.println(c);
      agent = agent.get_opposite();
    }
  }
}
