import java.util.ArrayList;
import java.util.List;

public class Main {
  public static void main(String[] args) {

    long start_time = System.currentTimeMillis();
    Color agent = Color.WHITE;
    ChessState c =ChessState.fromFenString("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    System.out.println(c.evaluate(Color.WHITE));
    SearchAgent s = new MultiThreadAgent(4);
//    while (!c.is_end_state(agent)) {
    for (int i = 0; i < 10; i++) {
      System.out.println(c);
      Action move = s.get_action(c, agent);
      c = c.get_successor_state(move, agent);
      System.out.println(move);
      System.out.println("Eval: " + c.evaluate(agent));
      c.print_evals();
      agent = agent.get_opposite();
    }
    System.out.println(c);
    System.out.println("Eval: " + c.evaluate(agent));
    c.print_evals();
    agent = agent.get_opposite();
    System.out.println("Time: " + (System.currentTimeMillis() - start_time));
  }
}
