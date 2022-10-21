from enum import Enum


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def get_opposite(self):
        return Color((self.value + 1) % 2)

    def __str__(self):
        return self.name[0]
