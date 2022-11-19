import java.util.Locale;

public enum Color {
  WHITE, BLACK;

  public Color get_opposite() {
    switch (this) {
      case WHITE -> {return BLACK;}
      case BLACK -> {return WHITE;}
    }
    throw new IllegalArgumentException("What???");
  }

  public static Color fromString(String color) {
    if (color.equalsIgnoreCase("white")) {
      return WHITE;
    }
    return BLACK;
  }

}


/*
from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def get_opposite(self):
        return Color((self.value + 1) % 2)

    def __str__(self):
        return self.name[0]

 */