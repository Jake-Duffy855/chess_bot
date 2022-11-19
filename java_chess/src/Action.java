import java.util.Objects;

public class Action {
  public Pos start_pos;
  public Pos end_pos;

  public Action(Pos start_pos, Pos end_pos) {
    this.start_pos = start_pos;
    this.end_pos = end_pos;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Action action = (Action) o;
    return start_pos.equals(action.start_pos) && end_pos.equals(action.end_pos);
  }

  @Override
  public String toString() {
    return "" + start_pos + " -> " + end_pos;
  }

  @Override
  public int hashCode() {
    return Objects.hash(start_pos, end_pos);
  }
}