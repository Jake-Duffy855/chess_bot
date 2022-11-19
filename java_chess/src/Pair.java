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
}
