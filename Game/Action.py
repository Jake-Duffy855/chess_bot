class Action:

    def __init__(self, start_pos: tuple[int, int], end_pos: tuple[int, int]):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __str__(self):
        return f'{self.start_pos} -> {self.end_pos}'
