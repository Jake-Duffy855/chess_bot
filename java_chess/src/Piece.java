public enum Piece {
  WHITE_PAWN(0),
  WHITE_KNIGHT(1),
  WHITE_BISHOP(2),
  WHITE_ROOK(3),
  WHITE_QUEEN(4),
  WHITE_KING(5),
  BLACK_PAWN(6),
  BLACK_KNIGHT(7),
  BLACK_BISHOP(8),
  BLACK_ROOK(9),
  BLACK_QUEEN(10),
  BLACK_KING(11),
  EMPTY(12);

  private final int value;

  private final static char[] STRING_REPS = {'♙', '♘', '♗', '♖', '♕', '♔', '♟', '♞', '♝', '♜', '♛', '♚', ' '};
  private final static int[] MATERIAL_VALUE = {1, 3, 3, 5, 9, 0, -1, -3, -3, -5, -9, 0, 0};
  private final static int[] SLIDING_NUMBERS = {2, 3, 4};

  private Piece(final int value) {
    this.value = value;
  }

  public Color get_color() {
    if (this.is_empty()) {
      throw new IllegalArgumentException("Blank doesn't have color");
    }
    if (value < 6) {
      return Color.WHITE;
    } else {
      return Color.BLACK;
    }
  }

  public boolean is_white() {
    return value < 6;
  }

  public boolean is_black() {
    return 12 > value && value >= 6;
  }

  public boolean is_color(Color color) {
    if (color == Color.WHITE) {
      return value < 6;
    }
    return 12 > value && value >= 6;
  }

  public int get_value() {
    return MATERIAL_VALUE[value];
  }

  public boolean is_pawn() {
    return value % 6 == 0 && value != 12;
  }

  public boolean is_knight() {
    return value % 6 == 1;
  }

  public boolean is_bishop() {
    return value % 6 == 2;
  }

  public boolean is_rook() {
    return value % 6 == 3;
  }

  public boolean is_queen() {
    return value % 6 == 4;
  }

  public boolean is_king() {
    return value % 6 == 5;
  }

  public boolean is_empty() {
    return value == 12;
  }

  public boolean is_sliding() {
    return value % 6 == 2 || value % 6 == 3 || value % 6 == 4;
  }

  public String toString() {
    return "" + STRING_REPS[value];
  }

  public static Piece fromString(char c) {
    switch (c) {
      case '♙': return WHITE_PAWN;
      case '♘': return WHITE_KNIGHT;
      case '♗': return WHITE_BISHOP;
      case '♖': return WHITE_ROOK;
      case '♕': return WHITE_QUEEN;
      case '♔': return WHITE_KING;
      case '♟': return BLACK_PAWN;
      case '♞': return BLACK_KNIGHT;
      case '♝': return BLACK_BISHOP;
      case '♜': return BLACK_ROOK;
      case '♛': return BLACK_QUEEN;
      case '♚': return BLACK_KING;
      case ' ': return EMPTY;
    }
    return null;
  }

}


/*
from Game.Color import *

from enum import Enum

STRING_REPS = ['♙', '♘', '♗', '♖', '♕', '♔', '♟', '♞', '♝', '♜', '♛', '♚', " "]
MATERIAL_VALUE = [1, 3, 3, 5, 9, 0, -1, -3, -3, -5, -9, 0, 0]
SLIDING_NUMBERS = {2, 3, 4}


class Piece(Enum)
    WHITE_PAWN = 0
    WHITE_KNIGHT = 1
    WHITE_BISHOP = 2
    WHITE_ROOK = 3
    WHITE_QUEEN = 4
    WHITE_KING = 5

    BLACK_PAWN = 6
    BLACK_KNIGHT = 7
    BLACK_BISHOP = 8
    BLACK_ROOK = 9
    BLACK_QUEEN = 10
    BLACK_KING = 11

    EMPTY = 12

    def get_color(self)
        if is_empty()
            raise ValueError("Blank doesn't have color")
        return Color.WHITE if value < 6 else Color.BLACK

    def is_white(self)
        return value < 6

    def is_black(self)
        return 12 > value >= 6

    def is_color(self, color Color)
        if color == Color.WHITE
            return value < 6
        return 12 > value >= 6

    def get_value(self)
        return MATERIAL_VALUE[value]

    def is_pawn(self)
        return value % 6 == 0 and value != 12

    def is_knight(self)
        return value % 6 == 1

    def is_bishop(self)
        return value % 6 == 2

    def is_rook(self)
        return value % 6 == 3

    def is_queen(self)
        return value % 6 == 4

    def is_king(self)
        return value % 6 == 5

    def is_empty(self)
        return value == 12

    def is_sliding(self)
        return value % 6 in SLIDING_NUMBERS

    def __str__(self)
        return STRING_REPS[value]


if __name__ == '__main__'
    print([str(m) for m in Piece.WHITE_KING.get_possible_moves_from((4, 4))])

 */