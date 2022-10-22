class Action:

    def __init__(self, start_pos: tuple[int, int], end_pos: tuple[int, int]):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __str__(self):
        return f'{self.start_pos} -> {self.end_pos}'

    def __eq__(self, other):
        return isinstance(other, Action) and self.start_pos == other.start_pos and self.end_pos == other.end_pos
