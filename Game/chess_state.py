from timeit import Timer

from Action import Action
from Piece import *
from Color import *
import random

EMT = EmptySquare()
WK = None
BK = None

# maybe for speed up in the future use a hash from loc to piece and piece type to list of loc???
# maybe not because there's not a lot of list searching and access is O(1) anyway
DEFAULT_BOARD = [
    [Rook(Black()), Knight(Black()), Bishop(Black()), Queen(Black()),
     King(Black()), Bishop(Black()), Knight(Black()), Rook(Black())],
    [Pawn(Black()) for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [Pawn(White()) for _ in range(8)],
    [Rook(White()), Knight(White()), Bishop(White()), Queen(White()),
     King(White()), Bishop(White()), Knight(White()), Rook(White())]
]


class ChessState:

    def __init__(self, pieces: list[list[Piece]], wcl=True, wcr=True, bcl=True, bcr=True, en_passant=()):
        self.pieces = pieces
        self.size = (len(pieces), len(pieces[0]))
        self.wcl = wcl
        self.wcr = wcr
        self.bcl = bcl
        self.bcr = bcr
        self.en_passant = en_passant

    def get_legal_moves(self, agent: Color) -> list[Action]:
        legal_moves = []
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                legal_moves.extend(
                    [action for action in piece.get_possible_moves_from((i, j)) if
                     self.__is_legal_move(action, agent) and piece.color == agent]
                )
        return legal_moves

    def get_successor_state(self, action: Action, agent: Color):
        if self.__is_legal_move(action, agent):
            new_pieces = self.__move_loc_to_loc(action.start_pos, action.end_pos)
            return ChessState(new_pieces)
        else:
            raise ValueError("Bruh")

    # move the piece in sloc to eloc regardless of if it's legal
    def __move_loc_to_loc(self, sloc, eloc) -> list[list[Piece]]:
        new_pieces = [[piece for piece in row] for row in self.pieces]
        si, sj = sloc
        ei, ej = eloc
        new_pieces[ei][ej] = self.get_piece_at(sloc)
        new_pieces[si][sj] = EMT
        if ei == 0 and new_pieces[ei][ej] == Pawn(White()):
            new_pieces[ei][ej] = Queen(White())
        elif ei == 7 and new_pieces[ei][ej] == Pawn(Black()):
            new_pieces[ei][ej] = Queen(Black())
        return new_pieces

    def __is_legal_move(self, action: Action, agent: Color) -> bool:
        sloc = action.start_pos
        eloc = action.end_pos
        si, sj = sloc
        ei, ej = eloc
        # moving piece off of board
        if min(sloc + eloc) < 0 or max(sloc[0], eloc[0]) >= self.size[0] or max(sloc[1], eloc[1]) >= self.size[1]:
            return False

        spiece = self.get_piece_at(sloc)
        epiece = self.get_piece_at(eloc)

        # moving wrong color piece or empty square
        if spiece == EMT or spiece.color != agent:
            return False
        # moving piece onto own piece
        if epiece != EMT and epiece.color == agent:
            return False

        # only knights can jump, i.e. other pieces can't move through other pieces
        if self.get_piece_at(sloc) != Knight(agent):
            num_in_between = max(abs(ei - si), abs(ej - sj))
            di = (ei - si) // num_in_between
            dj = (ej - sj) // num_in_between
            for idx in range(1, num_in_between):
                piece_in_between = self.get_piece_at((si + di * idx, sj + dj * idx))
                if piece_in_between != EMT:
                    return False

        # pawns can take diagonally, but not directly
        if spiece == Pawn(agent):
            if abs(ei - si) == 1 and abs(ej - sj) == 1:
                if epiece == EMT or epiece.color == spiece.color:
                    return False
            elif epiece != EMT:
                return False

        # move can't result in check
        if ChessState.is_in_check(self.__move_loc_to_loc(sloc, eloc), agent):
            # print(action)
            return False

        return True

    def is_in_check(new_pieces, agent):
        # Could be sped up if only the moving piece is checked and the files/diagonals that moving piece was from
        king_pos = None
        for i, row in enumerate(new_pieces):
            for j, piece in enumerate(row):
                if piece == King(agent):
                    king_pos = i, j
        if king_pos is None:
            raise ValueError("you can't take the king what??")
        # go up, down, left, right, diagonals see if there's an attacking piece
        ki, kj = king_pos
        opp = agent.get_opposite()
        # left
        for dj in range(1, kj + 1):
            if new_pieces[ki][kj - dj] != EMT:
                if new_pieces[ki][kj - dj] == Rook(opp) or new_pieces[ki][kj - dj] == Queen(opp):
                    return True
                else:
                    break
        # right
        for dj in range(1, 8 - kj):
            if new_pieces[ki][kj + dj] != EMT:
                if new_pieces[ki][kj + dj] == Rook(opp) or new_pieces[ki][kj + dj] == Queen(opp):
                    return True
                else:
                    break
        # up
        for di in range(1, ki + 1):
            if new_pieces[ki - di][kj] != EMT:
                if new_pieces[ki - di][kj] == Rook(opp) or new_pieces[ki - di][kj] == Queen(opp):
                    return True
                else:
                    break
        # down
        for di in range(1, 8 - ki):
            if new_pieces[ki + di][kj] != EMT:
                if new_pieces[ki + di][kj] == Rook(opp) or new_pieces[ki + di][kj] == Queen(opp):
                    return True
                else:
                    break
        # diag up right (dur)
        for d in range(1, min(ki + 1, 8 - kj)):
            if new_pieces[ki - d][kj + d] != EMT:
                if new_pieces[ki - d][kj + d] == Bishop(opp) or new_pieces[ki - d][kj + d] == Queen(opp):
                    return True
                else:
                    break
        # diag up left (dul)
        for d in range(1, min(ki + 1, kj + 1)):
            if new_pieces[ki - d][kj - d] != EMT:
                if new_pieces[ki - d][kj - d] == Bishop(opp) or new_pieces[ki - d][kj - d] == Queen(opp):
                    return True
                else:
                    break
        # diag down right (ddr)
        for d in range(1, min(8 - ki, 8 - kj)):
            if new_pieces[ki + d][kj + d] != EMT:
                if new_pieces[ki + d][kj + d] == Bishop(opp) or new_pieces[ki + d][kj + d] == Queen(opp):
                    return True
                else:
                    break
        # diag down left (ddl)
        for d in range(1, min(8 - ki, kj + 1)):
            if new_pieces[ki + d][kj - d] != EMT:
                if new_pieces[ki + d][kj - d] == Bishop(opp) or new_pieces[ki + d][kj - d] == Queen(opp):
                    return True
                else:
                    break

        # check for pawns
        if agent == White():
            if ki > 1 and (kj > 0 and new_pieces[ki - 1][kj - 1] == Pawn(Black()) or
                           kj < 7 and new_pieces[ki - 1][kj + 1] == Pawn(Black())):
                return True
        else:
            if ki < 6 and (kj > 0 and new_pieces[ki + 1][kj - 1] == Pawn(White()) or
                           kj < 7 and new_pieces[ki + 1][kj + 1] == Pawn(White())):
                return True
        # check knight positions
        knight_diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        for di, dj in knight_diffs:
            ni = ki + di
            nj = kj + dj
            if 0 <= ni < 8 and 0 <= nj < 8 and new_pieces[ni][nj] == Knight(opp):
                return True

        # can't be directly next to a king!
        for di in range(max(-ki, -1), min(8 - ki, 2)):
            for dj in range(max(-kj, -1), min(8 - kj, 2)):
                if new_pieces[ki + di][kj + dj] == King(opp):
                    return True

        # not in check!
        return False

    def is_win(self):
        # black has no moves and is in check
        return not self.get_legal_moves(Black()) and ChessState.is_in_check(self.pieces, Black())

    def is_lose(self):
        # white has no moves and is in check
        return not self.get_legal_moves(White()) and ChessState.is_in_check(self.pieces, White())

    def is_draw(self):
        return self.is_stalemate() or self.insufficient_material()

    def is_stalemate(self):
        return not self.get_legal_moves(White()) and not ChessState.is_in_check(self.pieces, White()) or \
               not self.get_legal_moves(Black()) and not ChessState.is_in_check(self.pieces, Black())

    def is_end_state(self, agent):
        return not self.get_legal_moves(agent)

    def insufficient_material(self):
        for row in self.pieces:
            for piece in row:
                if piece != EMT and piece != King(piece.color):
                    return False
        return True

    def get_piece_at(self, loc: tuple[int, int]) -> Piece:
        return self.pieces[loc[0]][loc[1]]

    def evaluate(self) -> float:
        return 1000 if self.is_win() else 0 - 1000 if self.is_lose() else 0

    def __get_king_pos(self, color: Color) -> tuple[int, int]:
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                if piece == King(color):
                    return i, j
        raise ValueError(f"Where the heck is the {color} king???")

    def __str__(self) -> str:
        result = "-" * 23 + "\n"
        for row in self.pieces:
            for piece in row:
                result += str(piece) + "  "
            result += "\n"
        result += "-" * 23
        return result


def run_with_seed(seed, do_print=False):
    # return win, loss, draw for white
    random.seed(seed)
    c = ChessState(DEFAULT_BOARD)
    moves = 0
    if do_print:
        print(c)
    while moves < 100:
        if moves % 2 == 0:
            a = White()
        else:
            a = Black()
        if c.is_end_state(a):
            break
        c = c.get_successor_state(random.choice(c.get_legal_moves(a)), a)
        if do_print:
            print(c)
        moves += 1
    if do_print:
        print(c.is_win(), c.is_lose(), c.is_draw())
    return c.is_win(), c.is_lose(), c.is_draw()


def get_interesting_seeds(n):
    for seed in range(n):
        if seed % 10 == 0:
            print(seed)
        try:
            win, loss, draw = run_with_seed(seed)
            if win or loss:
                print(seed, win, loss, draw)
        except ValueError as ve:
            if str(ve) != "you can't take the king what??":
                raise


def run_random():
    seed = int(1000 * random.random())
    run_with_seed(seed, True)
    print(seed)


if __name__ == '__main__':
    # t1 = Timer('run_with_seed(26)', 'from __main__ import run_with_seed')
    # print(t1.timeit(number=10))

    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        get_interesting_seeds(100)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

""" Notes
Moves left:
    Castling: needed
    en-passant: mehhhh
    choosing promotion: auto-queen is easier hehe
    
Only need one of each object, basically enum


important seeds:
    white blck draw
95 False True False
168 False True False
228 False True False
256 True False False
"""
