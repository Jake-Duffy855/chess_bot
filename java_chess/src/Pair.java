import java.util.Objects;

public class Pair<T, V> {
  private T x;
  private V y;


  public Pair(T x, V y) {
    this.x = x;
    this.y = y;
  }

  public T getFirst() {
    return x;
  }

  public V getSecond() {
    return y;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Pair<?, ?> pair = (Pair<?, ?>) o;
    return Objects.equals(x, pair.x) && Objects.equals(y, pair.y);
  }

  @Override
  public int hashCode() {
    return Objects.hash(x, y);
  }
}
