import java.util.ArrayList;
import java.util.List;

public class Main {
  public static void main(String[] args) {
    Color agent = Color.WHITE;
    ChessState c = new ChessState();
//    SearchAgent s = new SearchAgent(5);
//    System.out.println(c);
    List<ChessState> states = new ArrayList<>();
    states.add(c);
    for (int i = 0; i < 5; i++) {
      List<ChessState> newStates = new ArrayList<>();
      for (ChessState state : states) {
        List<Action> moves = state.get_legal_moves(agent);
        for (Action m : moves) {
          newStates.add(state.get_successor_state(m, agent));
        }
      }
      System.out.println(newStates.size());
      states = newStates;
      agent = agent.get_opposite();
    }
  }
}
