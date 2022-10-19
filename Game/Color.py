class Color:
    def get_opposite(self):
        pass


class White(Color):

    def __str__(self):
        return "W"

    def __eq__(self, other):
        return isinstance(other, White)

    def get_opposite(self):
        return Black()


class Black(Color):

    def __str__(self):
        return "B"

    def __eq__(self, other):
        return isinstance(other, Black)

    def get_opposite(self):
        return White()
