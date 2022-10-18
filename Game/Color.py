class Color:
    pass


class White(Color):

    def __str__(self):
        return "W"

    def __eq__(self, other):
        return isinstance(other, White)


class Black(Color):

    def __str__(self):
        return "B"

    def __eq__(self, other):
        return isinstance(other, Black)
