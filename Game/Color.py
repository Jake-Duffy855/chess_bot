class Color:
    pass


class White(Color):

    def __str__(self):
        return "W"

    def __eq__(self, other):
        return other is White


class Black(Color):

    def __str__(self):
        return "B"

    def __eq__(self, other):
        return other is Black
