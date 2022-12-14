import sys
import os

path = os.path.dirname(os.path.abspath(__file__))[0:-5]
sys.path.insert(0, path)

from Game.Piece import *
from Game.Action import *
import random

EMT = Piece.EMPTY
# count_calls = [0] * 8
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]

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

ITALIAN_BOARD = [
    [Piece.BLACK_ROOK, EMT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN, Piece.BLACK_KING, EMT,
     Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
    [Piece.BLACK_PAWN for _ in range(4)] + [EMT] + [Piece.BLACK_PAWN for _ in range(3)],
    [EMT, EMT, Piece.BLACK_KNIGHT, EMT, EMT, EMT, EMT, EMT],
    [EMT, EMT, Piece.BLACK_BISHOP, EMT, Piece.BLACK_PAWN, EMT, EMT, EMT],
    [EMT, EMT, Piece.WHITE_BISHOP, EMT, Piece.WHITE_PAWN, EMT, EMT, EMT],
    [EMT, EMT, EMT, EMT, EMT, Piece.WHITE_KNIGHT, EMT, EMT],
    [Piece.WHITE_PAWN for _ in range(4)] + [EMT] + [Piece.WHITE_PAWN for _ in range(3)],
    [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN, Piece.WHITE_KING, EMT,
     EMT, Piece.WHITE_ROOK]
]

NUM_PAWNS = 2
SMALL_GAME = [
    [EMT, EMT, EMT, EMT, Piece.BLACK_KING, EMT, EMT, EMT],
    [Piece.BLACK_PAWN for _ in range(NUM_PAWNS - 2)] + [EMT for _ in range(8 - NUM_PAWNS + 2)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT, EMT] + [Piece.WHITE_PAWN for _ in range(NUM_PAWNS - 1)] + [EMT for _ in range(8 - NUM_PAWNS - 1)],
    [EMT, EMT, EMT, EMT, Piece.WHITE_KING, EMT, EMT, EMT]
]

SMALL_QUEEN_GAME = [
    [EMT, EMT, EMT, EMT, Piece.BLACK_KING, EMT, EMT, EMT],
    [EMT, EMT] + [Piece.WHITE_QUEEN for _ in range(NUM_PAWNS - 1)] + [EMT for _ in range(8 - NUM_PAWNS - 1)],
    [EMT, EMT, EMT, EMT, Piece.WHITE_KING, EMT, EMT, EMT],
    [Piece.BLACK_PAWN for _ in range(NUM_PAWNS - 2)] + [EMT for _ in range(8 - NUM_PAWNS + 2)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],
    [EMT for _ in range(8)],

]
# up, down, left, right, dul, dur, ddl, ddr
move_diffs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
dist_to_edge = []
NUM_STATES_SAVED = 20
for gi in range(8):
    dist_to_edge.append([])
    for gj in range(8):
        u = gi
        d = 7 - gi
        l = gj
        r = 7 - gj
        dist_to_edge[gi].append([
            u, d, l, r, min(u, l), min(u, r), min(d, l), min(d, r)
        ])


class ChessState:

    def __init__(self, pieces: list[list[Piece]], wcl=True, wcr=True, bcl=True, bcr=True, en_passant=(),
                 white_king_pos=(7, 4), black_king_pos=(0, 4), whc=False, bhc=False, last_states=None):
        self.pieces = pieces
        self.size = (len(pieces), len(pieces[0]))
        self.wcl = wcl
        self.wcr = wcr
        self.bcl = bcl
        self.bcr = bcr
        self.en_passant = en_passant
        self.white_king_pos = white_king_pos
        self.black_king_pos = black_king_pos
        self.whc = whc
        self.bhc = bhc
        if last_states is None:
            self.last_states = []
        else:
            self.last_states = last_states
        # doesn't speed up
        # self.white_score = self.__evaluate(Color.WHITE)
        # self.black_score = self.__evaluate(Color.BLACK)

    def get_legal_moves(self, agent: Color) -> list[Action]:
        legal_moves = []
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                legal_moves.extend(
                    [action for action in self.get_possible_moves(piece, (i, j), agent) if
                     self.__faster_is_legal(action, agent)]
                )
        return legal_moves

    def get_possible_moves(self, piece: Piece, loc, agent: Color):
        if piece == EMT or not piece.is_color(agent):
            return []
        i, j = loc
        if piece.is_pawn():
            result = []
            step = 1 if piece.is_black() else -1
            home_row = 1 if piece.is_black() else 6
            # add double pawn push
            if i == home_row and self.pieces[i + step][j] == EMT and self.pieces[i + 2 * step][j] == EMT:
                result.append(Action(loc, (i + 2 * step, j)))
            # single push
            for dj in range(-1, 2):
                # valid push or valid take
                if dj == 0 and self.pieces[i + step][j] == EMT or dj != 0 and 0 <= j + dj < 8 and \
                        self.pieces[i + step][j + dj].is_color(agent.get_opposite()):
                    result.append(Action(loc, (i + step, j + dj)))
            return result
        # bishops, rooks, and queens
        elif piece.is_sliding():
            moves = []
            start_idx = 4 if piece.is_bishop() else 0
            end_idx = 4 if piece.is_rook() else 8
            for direction in range(start_idx, end_idx):
                for dist in range(dist_to_edge[i][j][direction]):
                    di, dj = move_diffs[direction]
                    new_i = i + di * (dist + 1)
                    new_j = j + dj * (dist + 1)
                    target_piece = self.pieces[new_i][new_j]
                    if target_piece.is_color(agent):
                        break
                    moves.append(Action(loc, (new_i, new_j)))
                    if target_piece.is_color(agent.get_opposite()):
                        break
            return moves
        elif piece.is_knight():
            diffs = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
            result = []
            for di, dj in diffs:
                if 0 <= (i + di) < 8 and 0 <= (j + dj) < 8 and not self.pieces[i + di][j + dj].is_color(agent):
                    result.append(Action(loc, (i + di, j + dj)))
            return result
        elif piece.is_king():
            result = []
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if 0 <= (i + di) < 8 and 0 <= (j + dj) < 8 and not self.pieces[i + di][j + dj].is_color(agent):
                        result.append(Action(loc, (i + di, j + dj)))
            # caslting back in
            result.extend([Action(loc, (i, j + 2)), Action(loc, (i, j - 2))])
            return result
        return []

    def get_successor_state(self, action: Action, agent: Color):
        if self.is_legal_move(action, agent):
            new_pieces = self.__move_loc_to_loc(action.start_pos, action.end_pos)
            # castle: move rook, still need to add checks for moved kings and moved rooks and moving through check
            spiece = self.pieces[action.start_pos[0]][action.start_pos[1]]
            new_white_king_pos = self.white_king_pos
            new_black_king_pos = self.black_king_pos
            new_wcl, new_wcr, new_bcl, new_bcr = self.wcl, self.wcr, self.bcl, self.bcr
            new_whc, new_bhc = self.whc, self.bhc
            if spiece.is_king():
                new_wcl, new_wcr, new_bcl, new_bcr = self.__update_castling(action)
                new_whc, new_bhc = self.__update_has_castled(action)
                if spiece.is_white():
                    new_white_king_pos = action.end_pos
                else:
                    new_black_king_pos = action.end_pos
            if spiece.is_rook():
                new_wcl, new_wcr, new_bcl, new_bcr = self.__update_castling(action)

            new_last_states = self.__get_new_last_states(agent)

            return ChessState(new_pieces, new_wcl, new_wcr, new_bcl, new_bcr, white_king_pos=new_white_king_pos,
                              black_king_pos=new_black_king_pos, whc=new_whc, bhc=new_bhc, last_states=new_last_states)
        else:
            raise ValueError("Bruh")

    def __get_new_last_states(self, agent: Color):
        if len(self.last_states) < NUM_STATES_SAVED:
            return self.last_states[:] + [self.to_fen(agent)]
        return self.last_states[1:] + [self.to_fen(agent)]

    def __update_castling(self, action):
        si, sj = action.start_pos
        new_wcl, new_wcr, new_bcl, new_bcr = self.wcl, self.wcr, self.bcl, self.bcr
        # if king moves, no more castling
        if self.pieces[si][sj].is_king():
            if self.pieces[si][sj].is_white():
                new_wcl = new_wcr = False
            else:
                new_bcl = new_bcr = False
        # if rook moves, no more castling that way
        elif action.start_pos == (0, 0):
            new_bcl = False
        elif action.start_pos == (0, 7):
            new_bcr = False
        elif action.start_pos == (7, 0):
            new_wcl = False
        elif action.start_pos == (7, 7):
            new_wcr = False
        return new_wcl, new_wcr, new_bcl, new_bcr

    def __update_has_castled(self, action):
        spiece = self.get_piece_at(action.start_pos)
        new_whc, new_bhc = self.whc, self.bhc
        # if king moves, no more castling
        if spiece.is_king() and abs(action.end_pos[1] - action.start_pos[1]) == 2:
            if spiece.is_white():
                new_whc = True
            else:
                new_bhc = True
        return new_whc, new_bhc

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

    def __faster_is_legal(self, action: Action, agent: Color) -> bool:
        sloc = action.start_pos
        eloc = action.end_pos
        si, sj = sloc
        ei, ej = eloc

        spiece = self.get_piece_at(sloc)

        # castling, might break if moved below check
        if spiece.is_king() and abs(ej - sj) == 2:
            if spiece.is_white():
                if ej - sj == 2 and not self.wcr or ej - sj == -2 and not self.wcl:
                    return False
            else:
                if ej - sj == 2 and not self.bcr or ej - sj == -2 and not self.bcl:
                    return False
            new_end = (ei, sj + (ej - sj) // 2)
            if ej - sj == 2:
                rook_start = (si, 7)
                rook_end = (si, 5)
            else:
                rook_start = (si, 0)
                rook_end = (si, 3)
            if not self.is_legal_move(Action(sloc, new_end), agent) or \
                    not self.is_legal_move(Action(rook_start, rook_end), agent):
                return False

        # move can't result in check
        king_pos = self.__get_king_pos(agent)
        if king_pos == sloc:
            king_pos = eloc
        if self.is_in_check(self.__move_loc_to_loc(sloc, eloc), agent, king_pos):
            return False

        # it's a legal move!
        return True

    def is_legal_move(self, action: Action, agent: Color) -> bool:
        # if its possible and legal
        sloc = action.start_pos
        possible_moves = self.get_possible_moves(self.pieces[sloc[0]][sloc[1]], sloc, agent)
        return action in possible_moves and self.__faster_is_legal(action, agent)

    def is_in_check(self, new_pieces: list[list[Piece]], agent: Color, king_pos) -> bool:
        # Could be sped up if only the moving piece is checked and the files/diagonals that moving piece was from

        if king_pos is None:
            raise ValueError("you can't take the king what??")
        # go up, down, left, right, diagonals see if there's an attacking piece
        ki, kj = king_pos
        opp = agent.get_opposite()
        # sliding moves attacking
        for direction in range(0, 8):
            for dist in range(dist_to_edge[ki][kj][direction]):
                di, dj = move_diffs[direction]
                new_i = ki + di * (dist + 1)
                new_j = kj + dj * (dist + 1)
                target_piece = new_pieces[new_i][new_j]
                if target_piece != EMT:
                    if target_piece.is_color(opp) and (
                            target_piece.is_queen() or direction < 4 and target_piece.is_rook() or direction >= 4 and
                            target_piece.is_bishop()):
                        return True
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

    def __get_king_pos(self, agent: Color):
        if agent == Color.WHITE:
            return self.white_king_pos
        return self.black_king_pos

    def is_win(self):
        # black has no moves and is in check
        return not self.get_legal_moves(Color.BLACK) and self.is_in_check(self.pieces, Color.BLACK, self.black_king_pos)

    def is_lose(self):
        # white has no moves and is in check
        return not self.get_legal_moves(Color.WHITE) and self.is_in_check(self.pieces, Color.WHITE, self.white_king_pos)

    def is_draw(self, agent: Color):
        return self.is_stalemate() or self.insufficient_material() or self.is_repetition(agent)

    def is_repetition(self, agent: Color):
        return self.last_states.count(self.to_fen(agent)) >= 2

    def is_stalemate(self):
        return not self.get_legal_moves(Color.WHITE) and \
               not self.is_in_check(self.pieces, Color.WHITE, self.white_king_pos) or \
               not self.get_legal_moves(Color.BLACK) and \
               not self.is_in_check(self.pieces, Color.BLACK, self.black_king_pos)

    def is_end_state(self, agent):
        return not self.get_legal_moves(agent) or self.insufficient_material() or self.is_repetition(agent)

    def insufficient_material(self):
        for row in self.pieces:
            for piece in row:
                if not piece.is_king() and piece != EMT:
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
            return (1000 if self.is_win() else 0) - (1000 if self.is_lose() else 0)
        return self.__get_material() + \
               10 * self.__castle_eval() + \
               0.1 * self.__piece_activity() + \
               self.__get_endgame_multiplier() * (
                       self.__pawn_distance() +
                       self.__king_activity() * 0.2)

    def __piece_activity(self):
        # bad to have bishop and knight on back row
        total = 0
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                if piece.is_knight() or piece.is_bishop():
                    if piece.is_white() and i == 7:
                        total -= 1
                    elif piece.is_black() and i == 0:
                        total += 1
        return total

    def __castle_eval(self):
        # one point if you have castled
        return (1 if self.whc else 0) - (1 if self.bhc else 0)

    def __get_endgame_multiplier(self):
        # endgame evaluations are higher weighted when there are fewer pieces on the board
        return 1 - self.__get_num_pieces() / 16

    def __get_num_pieces(self):
        # how many pieces are left on the board
        total = 0
        for row in self.pieces:
            for piece in row:
                if piece != Piece.EMPTY:
                    total += 1

        return total

    def __pawn_distance(self):
        # how much further has white pushed their pawns
        total = 0
        for i, row in enumerate(self.pieces):
            for j, piece in enumerate(row):
                if piece.is_pawn():
                    if piece.is_white():
                        total += (7 - i)
                    else:
                        total -= i
        return total

    def __king_activity(self):
        wi, wj = self.white_king_pos
        bi, bj = self.black_king_pos
        return -abs(4 - wi) - abs(4 - wj) + abs(4 - bi) + abs(4 - bj)

    def to_fen(self, agent: Color):
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        result = ""
        for row in self.pieces:
            num_empty = 0
            for piece in row:
                if piece == Piece.EMPTY:
                    num_empty += 1
                else:
                    if num_empty > 0:
                        result += str(num_empty)
                        num_empty = 0
                    result += piece.fen_value()
            if num_empty > 0:
                result += str(num_empty)
            result += "/"
        result = result[:-1] + (" w " if agent == Color.WHITE else " b ")
        # castling
        if not (self.wcl or self.wcr or self.bcl or self.bcr):
            result += "-"
        result += "K" if self.wcr else ""
        result += "Q" if self.wcl else ""
        result += "k" if self.bcr else ""
        result += "q" if self.bcl else ""
        # ******* this should be different but it's unused ******
        result += " - 0 1"
        return result

    def __str__(self) -> str:
        result = "-" * 23 + "\n"
        for row in self.pieces:
            for piece in row:
                result += str(piece) + "  "
            result += "\n"
        result += "-" * 23
        return result

    def __hash__(self) -> int:
        return self.__str__().__hash__()


def run_with_seed(seed, do_print=False):
    # return win, loss, draw for white
    random.seed(seed)
    c = ChessState(DEFAULT_BOARD)
    a = Color.WHITE
    if do_print:
        print(c)
    for _ in range(200):
        if c.is_end_state(a):
            break
        c = c.get_successor_state(random.choice(c.get_legal_moves(a)), a)
        if do_print:
            print(c)
        a = a.get_opposite()
    if do_print:
        print(c.is_win(), c.is_lose(), c.is_draw(a))
    return c.is_win(), c.is_lose(), c.is_draw(a)


if __name__ == '__main__':
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        run_with_seed(1, False)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

""" Notes
Moves left:
    en-passant: mehhhh
    choosing promotion: auto-queen is easier hehe
    castling isi broken again add back to possible moves
"""
