from timeit import Timer

from Game.Color import *
from Game.Piece import *
from Game.Action import *
import random

EMT = Piece.EMPTY

# maybe for speed up in the future use a hash from loc to piece and piece type to list of loc???
# maybe not because there's not a lot of list searching and access is O(1) anyway
DEFAULT_BOARD = [
    [Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
     Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
    [Piece.BLACK_PAWN for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [Piece.WHITE_PAWN for _ in range(8)],
    [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
     Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK]
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
                    [action for action in self.get_possible_moves(piece, (i, j)) if
                     self.is_legal_move(action, agent) and piece.is_color(agent)]
                )
        return legal_moves

    def get_possible_moves(self, piece: Piece, loc):
        i, j = loc
        if piece.is_pawn():
            if piece.is_black():
                step = 1
                double = [Action(loc, (i + 2 * step, j))] if i == 1 else []
            else:
                step = -1
                double = [Action(loc, (i + 2 * step, j))] if i == 6 else []
            return [Action(loc, (i + step, j)), Action(loc, (i + step, j + 1)), Action(loc, (i + step, j - 1))] + double
        elif piece.is_knight():
            diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
            return [Action(loc, (i + di, j + dj)) for di, dj in diffs]
        elif piece.is_bishop():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs]
        elif piece.is_rook():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
        elif piece.is_queen():
            diffs = [diff for diff in range(-max(i, j), 8 - min(i, j)) if diff != 0]
            return [Action(loc, (i + d, j + d)) for d in diffs] + [Action(loc, (i + d, j - d)) for d in diffs] + [
                Action(loc, (i + d, j)) for d in diffs] + [Action(loc, (i, j + d)) for d in diffs]
        elif piece.is_king():
            return [Action(loc, (i + di, j + dj)) for di in range(-1, 2) for dj in range(-1, 2) if
                    di != 0 or dj != 0] + [Action(loc, (i, j + 2)), Action(loc, (i, j - 2))]
        return []

    def get_successor_state(self, action: Action, agent: Color):
        if self.is_legal_move(action, agent):
            new_pieces = self.__move_loc_to_loc(action.start_pos, action.end_pos)
            # castle: move rook, still need to add checks for moved kings and moved rooks and moving through check
            spiece = self.pieces[action.start_pos[0]][action.start_pos[1]]
            if spiece.is_king() or spiece.is_rook():
                self.__update_castling(action)

            return ChessState(new_pieces, self.wcl, self.wcr, self.bcl, self.bcr)
        else:
            raise ValueError("Bruh")

    def __update_castling(self, action):
        si, sj = action.start_pos
        # if king moves, no more castling
        if self.pieces[si][sj].is_king():
            if self.pieces[si][sj].is_white():
                self.wcl = self.wcr = False
            else:
                self.bcl = self.bcr = False
        # if rook moves, no more castling that way
        elif action.start_pos == (0, 0):
            self.bcl = False
        elif action.start_pos == (0, 7):
            self.bcr = False
        elif action.start_pos == (7, 0):
            self.wcl = False
        elif action.start_pos == (7, 7):
            self.wcr = False

    # move the piece in sloc to eloc regardless of if it's legal
    def __move_loc_to_loc(self, sloc, eloc) -> list[list[Piece]]:
        new_pieces = [[piece for piece in row] for row in self.pieces]
        si, sj = sloc
        ei, ej = eloc
        spiece = new_pieces[si][sj]
        new_pieces[ei][ej] = self.get_piece_at(sloc)
        new_pieces[si][sj] = EMT
        # promote to queen
        if ei == 0 and new_pieces[ei][ej] == Piece.WHITE_PAWN:
            new_pieces[ei][ej] = Piece.WHITE_QUEEN
        elif ei == 7 and new_pieces[ei][ej] == Piece.BLACK_PAWN:
            new_pieces[ei][ej] = Piece.BLACK_QUEEN

        # castle: move rook
        if spiece.is_king() and abs(ej - sj) == 2:
            if ej - sj == 2:
                # print(new_pieces[ei][ej + 1])
                new_pieces[ei][ej - 1] = new_pieces[ei][ej + 1]
                new_pieces[ei][ej + 1] = EMT
            else:
                new_pieces[ei][ej + 1] = new_pieces[ei][ej - 2]
                new_pieces[ei][ej - 2] = EMT

        return new_pieces

    def is_legal_move(self, action: Action, agent: Color) -> bool:
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
        if spiece == EMT or not spiece.is_color(agent):
            return False

        # moving piece onto own piece
        if epiece != EMT and epiece.is_color(agent):
            return False

        # only knights can jump, i.e. other pieces can't move through other pieces
        if not self.get_piece_at(sloc).is_knight():
            num_in_between = max(abs(ei - si), abs(ej - sj))
            di = (ei - si) // num_in_between
            dj = (ej - sj) // num_in_between
            for idx in range(1, num_in_between):
                piece_in_between = self.get_piece_at((si + di * idx, sj + dj * idx))
                if piece_in_between != EMT:
                    return False

        # pawns can take diagonally, but not directly
        if spiece.is_pawn():
            if abs(ei - si) == 1 and abs(ej - sj) == 1:
                if epiece == EMT or epiece.is_white() == spiece.is_white():
                    return False
            elif epiece != EMT:
                return False

        # castling, might break if moved below check
        if spiece.is_king() and abs(ej - sj) == 2:
            if spiece.is_white():
                if ej - sj == 2 and not self.wcr or ej - sj == -2 and not self.wcl:
                    return False
            else:
                if ej - sj == 2 and not self.bcr or ej - sj == -2 and not self.bcl:
                    return False
            new_end = (ei, sj + (ej - sj) // 2)
            if not self.is_legal_move(Action(sloc, new_end), agent):
                return False
            if self.is_in_check(self.pieces, spiece.get_color()):
                return False

        # move can't result in check
        if self.is_in_check(self.__move_loc_to_loc(sloc, eloc), agent):
            return False

        # it's a legal move!
        return True

    def is_in_check(self, new_pieces: list[list[Piece]], agent: Color):
        # Could be sped up if only the moving piece is checked and the files/diagonals that moving piece was from
        king_pos = None
        for i, row in enumerate(new_pieces):
            for j, piece in enumerate(row):
                if piece.is_king() and piece.is_color(agent):
                    king_pos = i, j
        if king_pos is None:
            raise ValueError("you can't take the king what??")
        # go up, down, left, right, diagonals see if there's an attacking piece
        ki, kj = king_pos
        opp = agent.get_opposite()
        # left
        for dj in range(1, kj + 1):
            piece = new_pieces[ki][kj - dj]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_rook() or piece.is_queen()):
                    return True
                else:
                    break
        # right
        for dj in range(1, 8 - kj):
            piece = new_pieces[ki][kj + dj]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_rook() or piece.is_queen()):
                    return True
                else:
                    break
        # up
        for di in range(1, ki + 1):
            piece = new_pieces[ki - di][kj]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_rook() or piece.is_queen()):
                    return True
                else:
                    break
        # down
        for di in range(1, 8 - ki):
            piece = new_pieces[ki + di][kj]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_rook() or piece.is_queen()):
                    return True
                else:
                    break
        # diag up right (dur)
        for d in range(1, min(ki + 1, 8 - kj)):
            piece = new_pieces[ki - d][kj + d]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_bishop() or piece.is_queen()):
                    return True
                else:
                    break
        # diag up left (dul)
        for d in range(1, min(ki + 1, kj + 1)):
            piece = new_pieces[ki - d][kj - d]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_bishop() or piece.is_queen()):
                    return True
                else:
                    break
        # diag down right (ddr)
        for d in range(1, min(8 - ki, 8 - kj)):
            piece = new_pieces[ki + d][kj + d]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_bishop() or piece.is_queen()):
                    return True
                else:
                    break
        # diag down left (ddl)
        for d in range(1, min(8 - ki, kj + 1)):
            piece = new_pieces[ki + d][kj - d]
            if piece != EMT:
                if piece.is_color(opp) and (piece.is_bishop() or piece.is_queen()):
                    return True
                else:
                    break

        # check for pawns
        if agent == Color.WHITE:
            if ki > 1 and (kj > 0 and new_pieces[ki - 1][kj - 1] == Piece.BLACK_PAWN or
                           kj < 7 and new_pieces[ki - 1][kj + 1] == Piece.BLACK_PAWN):
                return True
        else:
            if ki < 6 and (kj > 0 and new_pieces[ki + 1][kj - 1] == Piece.WHITE_PAWN or
                           kj < 7 and new_pieces[ki + 1][kj + 1] == Piece.WHITE_PAWN):
                return True
        # check knight positions
        knight_diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        for di, dj in knight_diffs:
            ni = ki + di
            nj = kj + dj
            if 0 <= ni < 8 and 0 <= nj < 8 and new_pieces[ni][nj].is_knight() and new_pieces[ni][nj].is_color(opp):
                return True

        # can't be directly next to a king!
        for di in range(max(-ki, -1), min(8 - ki, 2)):
            for dj in range(max(-kj, -1), min(8 - kj, 2)):
                if new_pieces[ki + di][kj + dj].is_king() and new_pieces[ki + di][kj + dj].is_color(opp):
                    return True

        # not in check!
        return False

    def is_win(self):
        # black has no moves and is in check
        return not self.get_legal_moves(Color.BLACK) and self.is_in_check(self.pieces, Color.BLACK)

    def is_lose(self):
        # white has no moves and is in check
        return not self.get_legal_moves(Color.WHITE) and self.is_in_check(self.pieces, Color.WHITE)

    def is_draw(self):
        return self.is_stalemate() or self.insufficient_material()

    def is_stalemate(self):
        return not self.get_legal_moves(Color.WHITE) and not self.is_in_check(self.pieces, Color.WHITE) or \
               not self.get_legal_moves(Color.BLACK) and not self.is_in_check(self.pieces, Color.BLACK)

    def is_end_state(self, agent):
        return not self.get_legal_moves(agent)

    def insufficient_material(self):
        for row in self.pieces:
            for piece in row:
                if piece.is_king() and piece != EMT:
                    return False
        return True

    def get_piece_at(self, loc: tuple[int, int]) -> Piece:
        return self.pieces[loc[0]][loc[1]]

    def __get_material(self):
        score = 0
        for row in self.pieces:
            for piece in row:
                score += piece.get_value()
        return score

    def evaluate(self, agent) -> float:
        if self.is_end_state(agent):
            return 1000 if self.is_win() else 0 - 1000 if self.is_lose() else 0
        return self.__get_material()

    def __get_king_pos(self, color: Color) -> tuple[int, int]:
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                if piece.is_king() and piece.is_color(color):
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
            a = Color.WHITE
        else:
            a = Color.BLACK
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
        # get_interesting_seeds(10)
        run_with_seed(256, True)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

""" Notes
Moves left:
    en-passant: mehhhh
    choosing promotion: auto-queen is easier hehe
"""
