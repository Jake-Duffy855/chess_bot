import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ChessState {
  private Piece[][] pieces;
  private boolean wcl;
  private boolean wcr;
  private boolean bcl;
  private boolean bcr;
  private Pos white_king_pos;
  private Pos black_king_pos;
  private boolean whc;
  private boolean bhc;
  private List<String> last_states;
  private final int NUM_STATES_SAVED = 20;

  // up, down, left, right, dul, dur, ddl, ddr
  private final Pos[] move_diffs = {new Pos(-1, 0), new Pos(1, 0), new Pos(0, -1), new Pos(0, 1), new Pos(-1, -1), new Pos(-1, 1), new Pos(1, -1), new Pos(1, 1)};
  private final int[][][] dist_to_edge = new int[8][8][8];

  public static final Piece[][] DEFAULT_BOARD = {
          {Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
                  Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK},
          {Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN, Piece.BLACK_PAWN},
          {Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY},
          {Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY},
          {Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY},
          {Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY},
          {Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN, Piece.WHITE_PAWN},
          {Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
                  Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK}
  };

  public ChessState(Piece[][] pieces, boolean wcl, boolean wcr, boolean bcl, boolean bcr, Pos white_king_pos,
                    Pos black_king_pos, boolean whc, boolean bhc, List<String> last_states) {
    this.pieces = pieces;
    this.wcl = wcl;
    this.wcr = wcr;
    this.bcl = bcl;
    this.bcr = bcr;
    this.white_king_pos = white_king_pos;
    this.black_king_pos = black_king_pos;
    this.whc = whc;
    this.bhc = bhc;
    this.last_states = new ArrayList<>();
    if (last_states != null) {
      this.last_states.addAll(last_states);
    }
    initDistToEdge();
  }

  public static void main(String[] args) {
//    args = new String[] {"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "white"};
    ChessState c = ChessState.fromFenString(args[0]);
    Color agent = Color.fromString(args[1]);
//    System.out.println(c.get_king_pos(agent));
//    System.out.println(c);
//    System.out.println(depth);
//    System.out.println(agent);
    System.out.println(c.get_legal_moves(agent));

//    ChessState c = new ChessState();
//    System.out.println(c);
//    Color agent = Color.WHITE;
//    for (int i = 0; i < 20; i++) {
//      if (agent == Color.WHITE) {
//        c = c.get_successor_state(c.get_legal_moves(agent).get(c.get_legal_moves(agent).size() - 1), agent);
//      } else {
//        c = c.get_successor_state(c.get_legal_moves(agent).get(0), agent);
//      }
//      System.out.println(c);
//      agent = agent.get_opposite();
//      System.out.println(c.is_end_state(agent));
//    }
  }

  public ChessState() {
    this(DEFAULT_BOARD);
  }

  public ChessState(Piece[][] pieces) {
    this(pieces, true, true, true, true, new Pos(7, 4), new Pos(0, 4), false, false, null);
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        if (pieces[i][j].is_king()) {
          if (pieces[i][j].is_white()) {
            white_king_pos = new Pos(i, j);
          } else {
            black_king_pos = new Pos(i, j);
          }
        }
      }
    }
  }

  public static ChessState fromFenString(String fenString) {
    String[] parts = fenString.split(" ");
    String pieceString = parts[0];
//    String turn = parts[1];
    String castlingRights = parts[2];
//    String enPassant = parts[3];
//    String halfMove = parts[4];
//    String fullMove = parts[5];
    boolean wcl = castlingRights.contains("Q");
    boolean wcr = castlingRights.contains("K");
    boolean bcl = castlingRights.contains("q");
    boolean bcr = castlingRights.contains("k");

    Piece[][] pieces = new Piece[8][8];
    Pos wkp = null;
    Pos bkp = null;
    int i = 0;
    int j = 0;
    for (char p : pieceString.toCharArray()) {
      if (p == '/') {
        i += 1;
        j = 0;
      } else if (Character.isDigit(p)) {
        for (int idx = 0; idx < Character.getNumericValue(p); idx++) {
          pieces[i][j] = Piece.EMPTY;
          j += 1;
        }
      } else {
        if (p == 'K') wkp = new Pos(i, j);
        if (p == 'k') bkp = new Pos(i, j);
        pieces[i][j] = Piece.fromFenString(p);
        j += 1;
      }
    }
    return new ChessState(pieces, wcl, wcr, bcl, bcr, wkp, bkp, false, false, null);
  }

  private void initDistToEdge() {
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        int u = i;
        int d = 7 - i;
        int l = j;
        int r = 7 - j;
        dist_to_edge[i][j] = new int[]{u, d, l, r, Math.min(u, l), Math.min(u, r), Math.min(d, l), Math.min(d, r)};
      }
    }
  }

  public List<Action> get_legal_moves(Color agent) {
    ArrayList<Action> legal_moves = new ArrayList<>();
    for (int i = 0; i < pieces.length; i++) {
      for (int j = 0; j < pieces[i].length; j++) {
        for (Action action : get_possible_moves(pieces[i][j], new Pos(i, j), agent)) {
          if (pieces[i][j].is_color(agent) && faster_is_legal(action, agent)) {
            legal_moves.add(action);
          }
        }
      }
    }
    return legal_moves;
  }

  public List<Action> get_possible_moves(Piece piece, Pos loc, Color agent) {
    if (piece == Piece.EMPTY || !piece.is_color(agent)) {
      return new ArrayList<>();
    }
    int i = loc.x;
    int j = loc.y;
    if (piece.is_pawn()) {
      List<Action> moves = new ArrayList<>();
      int step = 1;
      int home_row = 1;
      if (piece.is_white()) {
        step = -1;
        home_row = 6;
      }
      // add double push
      if (i == home_row && pieces[i + step][j] == Piece.EMPTY && pieces[i + 2 * step][j] == Piece.EMPTY) {
        moves.add(new Action(loc, new Pos(i + 2 * step, j)));
      }
      for (int dj = -1; dj < 2; dj++) {
        // valid push or valid take
        if (dj == 0 && pieces[i + step][j] == Piece.EMPTY || dj != 0 && 0 <= j + dj && j + dj < 8 &&
                pieces[i + step][j + dj].is_color(agent.get_opposite())) {
          moves.add(new Action(loc, new Pos(i + step, j + dj)));
        }
      }
      return moves;
      //bishops, rooks, and queens
    } else if (piece.is_sliding()) {
      List<Action> moves = new ArrayList<>();
      int start_idx = piece.is_bishop() ? 4 : 0;
      int end_idx = piece.is_rook() ? 4 : 8;
      for (int direction = start_idx; direction < end_idx; direction++) {
        for (int dist = 0; dist < dist_to_edge[i][j][direction]; dist++) {
          int di = move_diffs[direction].x;
          int dj = move_diffs[direction].y;
          int new_i = i + di * (dist + 1);
          int new_j = j + dj * (dist + 1);
          Piece target_piece = pieces[new_i][new_j];
          if (target_piece.is_color(agent)) {
            break;
          }
          moves.add(new Action(loc, new Pos(new_i, new_j)));
          if (target_piece.is_color(agent.get_opposite())) {
            break;
          }
        }
      }
      return moves;
    } else if (piece.is_knight()) {
      Pos[] diffs = {new Pos(-1, -2), new Pos(-2, -1), new Pos(-2, 1), new Pos(-1, 2), new Pos(1, 2), new Pos(2, 1), new Pos(2, -1), new Pos(1, -2)};
      List<Action> moves = new ArrayList<>();
      for (Pos diff : diffs) {
        int di = diff.x;
        int dj = diff.y;
        if (0 <= (i + di) && (i + di) < 8 && 0 <= (j + dj) && (j + dj) < 8 && !pieces[i + di][j + dj].is_color(agent)) {
          moves.add(new Action(loc, new Pos(i + di, j + dj)));
        }
      }
      return moves;
    } else if (piece.is_king()) {
      List<Action> moves = new ArrayList<>();
      for (int di = -1; di < 2; di++) {
        for (int dj = -1; dj < 2; dj++) {
          if (0 <= (i + di) && (i + di) < 8 && 0 <= (j + dj) && (j + dj) < 8 && !pieces[i + di][j + dj].is_color(agent)) {
            moves.add(new Action(loc, new Pos(i + di, j + dj)));
          }
        }
      }
      moves.add(new Action(loc, new Pos(i, j + 2)));
      moves.add(new Action(loc, new Pos(i, j - 2)));
      return moves;
    }
    return new ArrayList<Action>();
  }

  public ChessState get_successor_state(Action action, Color agent) {
    if (is_legal_move(action, agent)) {
      Piece[][] newPieces = move_loc_to_loc(action.start_pos, action.end_pos);
      // castle: move rook, still need to add checks for moved kings and moved rooks and moving through check??
      Piece spiece = get_piece_at(action.start_pos);
      Pos new_white_king_pos = white_king_pos;
      Pos new_black_king_pos = black_king_pos;
      boolean new_wcl = wcl;
      boolean new_wcr = wcr;
      boolean new_bcl = bcl;
      boolean new_bcr = bcr;
      Pair<Boolean, Boolean> updated_has_castled = update_has_castled(action);
      if (spiece.is_king() || spiece.is_rook()) {
        boolean[] updated_castling = update_casting(action);
        new_wcl = updated_castling[0];
        new_wcr = updated_castling[1];
        new_bcl = updated_castling[2];
        new_bcr = updated_castling[3];
      }
      if (spiece.is_king()) {
        if (spiece.is_white()) {
          new_white_king_pos = action.end_pos;
        } else {
          new_black_king_pos = action.end_pos;
        }
      }

      return new ChessState(newPieces, new_wcl, new_wcr, new_bcl, new_bcr, new_white_king_pos, new_black_king_pos,
              updated_has_castled.getFirst(), updated_has_castled.getSecond(), get_updated_last_moves(agent));
    } else {
      System.out.println(this);
      System.out.println(action);
      System.out.println(get_legal_moves(agent));
      System.out.println(get_king_pos(agent));
      throw new IllegalArgumentException("bruh");
    }
  }

  public void set_last_states(List<String> last_states) {
    // ONLY CALLED IN THE IO BETWEEN JAVA AND PYTHON
    this.last_states = last_states;
  }

  private List<String> get_updated_last_moves(Color agent) {
    List<String> result = new ArrayList<>(last_states);
    if (last_states.size() >= NUM_STATES_SAVED) result.remove(0);
    result.add(toFenString(agent));
    return result;
  }

  private Pair<Boolean, Boolean> update_has_castled(Action action) {
    Piece spiece = get_piece_at(action.start_pos);
    boolean new_whc = whc;
    boolean new_bhc = bhc;
    // if king moves, no more castling
    if (spiece.is_king() && Math.abs(action.end_pos.y - action.start_pos.y) == 2) {
      if (spiece.is_white()) {
        new_whc = true;
      } else {
        new_bhc = true;
      }
    }
    return new Pair<>(new_whc, new_bhc);
  }

  private boolean[] update_casting(Action action) {

    int si = action.start_pos.x;
    int sj = action.start_pos.y;
    boolean new_wcl = wcl;
    boolean new_wcr = wcr;
    boolean new_bcl = bcl;
    boolean new_bcr = bcr;
    // if king moves, no more castling
    if (get_piece_at(action.start_pos).is_king()) {
      if (get_piece_at(action.start_pos).is_white()) {
        new_wcl = false;
        new_wcr = false;
      } else {
        new_bcl = false;
        new_bcr = false;
      }
    } else if (si == 0 && sj == 0) {
      new_bcl = false;
    } else if (si == 0 && sj == 7) {
      new_bcr = false;
    } else if (si == 7 && sj == 0) {
      new_wcl = false;
    } else if (si == 7 && sj == 7) {
      new_wcr = false;
    }
    return new boolean[]{new_wcl, new_wcr, new_bcl, new_bcr};
  }

  private Piece[][] move_loc_to_loc(Pos sloc, Pos eloc) {
    Piece[][] newPieces = new Piece[8][8];
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        newPieces[i][j] = pieces[i][j];
      }
    }
    int si = sloc.x;
    int sj = sloc.y;
    int ei = eloc.x;
    int ej = eloc.y;
    Piece spiece = get_piece_at(sloc);
    newPieces[ei][ej] = spiece;
    newPieces[si][sj] = Piece.EMPTY;
    // promote to queen
    if (ei == 0 && newPieces[ei][ej] == Piece.WHITE_PAWN) {
      newPieces[ei][ej] = Piece.WHITE_QUEEN;
    } else if (ei == 7 && newPieces[ei][ej] == Piece.BLACK_PAWN) {
      newPieces[ei][ej] = Piece.BLACK_QUEEN;
    }
    // castle: move rook
    if (spiece.is_king() && Math.abs(ej - sj) == 2) {
      if (ej - sj == 2) {
        newPieces[ei][ej - 1] = newPieces[ei][ej + 1];
        newPieces[ei][ej + 1] = Piece.EMPTY;
      } else {
        newPieces[ei][ej + 1] = newPieces[ei][ej - 2];
        newPieces[ei][ej - 2] = Piece.EMPTY;
      }
    }
    return newPieces;
  }

  public boolean is_legal_move(Action action, Color agent) {
    Pos sloc = action.start_pos;
    List<Action> possible_moves = get_possible_moves(get_piece_at(sloc), sloc, agent);
    return possible_moves.contains(action) && faster_is_legal(action, agent);
  }

  private boolean faster_is_legal(Action action, Color agent) {

    Pos sloc = action.start_pos;
    Pos eloc = action.end_pos;
    int si = sloc.x;
    int sj = sloc.y;
    int ei = eloc.x;
    int ej = eloc.y;

    Piece spiece = get_piece_at(sloc);

    // castling, might break if moved below check
    if (spiece.is_king() && Math.abs(ej - sj) == 2) {
      if (spiece.is_white()) {
        if (ej - sj == 2 && !wcr || ej - sj == -2 && !wcl) {
          return false;
        }
      } else {
        if (ej - sj == 2 && !bcr || ej - sj == -2 && !bcl) {
          return false;
        }
      }
      Pos newEnd = new Pos(ei, sj + (ej - sj) / 2);
      Pos rookStart;
      Pos rookEnd;
      if (ej - sj == 2) {
        rookStart = new Pos(si, 7);
        rookEnd = new Pos(si, 5);
      } else {
        rookStart = new Pos(si, 0);
        rookEnd = new Pos(si, 3);
      }
      if (!is_legal_move(new Action(sloc, newEnd), agent) || !is_legal_move(new Action(rookStart, rookEnd), agent)) {
        return false;
      }
    }

    // move can't result in check
    Pos king_pos = get_king_pos(agent);
    if (king_pos.equals(sloc)) {
//      System.out.println("book");
      king_pos = eloc;
    }
    if (is_in_check(move_loc_to_loc(sloc, eloc), agent, king_pos)) {
      return false;
    }
    // it's a legal move!
    return true;
  }

  public Pos get_king_pos(Color agent) {
    if (agent == Color.WHITE) {
      return white_king_pos;
    }
    return black_king_pos;
  }

  public boolean is_in_check(Piece[][] new_pieces, Color agent, Pos king_pos) {
    int ki = king_pos.x;
    int kj = king_pos.y;
    Color opp = agent.get_opposite();
    for (int direction = 0; direction < 8; direction++) {
      for (int dist = 0; dist < dist_to_edge[ki][kj][direction]; dist++) {
        int di = move_diffs[direction].x;
        int dj = move_diffs[direction].y;
        int new_i = ki + di * (dist + 1);
        int new_j = kj + dj * (dist + 1);
        Piece target_piece = new_pieces[new_i][new_j];
        if (target_piece != Piece.EMPTY) {
          if (target_piece.is_color(opp) && (target_piece.is_queen() || direction < 4 && target_piece.is_rook() ||
                  direction >= 4 && target_piece.is_bishop())) {
            return true;
          }
          break;
        }
      }
    }
    // check for pawns
    if (agent == Color.WHITE) {
      if (ki > 1 && (kj > 0 && new_pieces[ki - 1][kj - 1] == Piece.BLACK_PAWN ||
              kj < 7 && new_pieces[ki - 1][kj + 1] == Piece.BLACK_PAWN)) {
        return true;
      }
    } else {
      if (ki < 6 && (kj > 0 && new_pieces[ki + 1][kj - 1] == Piece.WHITE_PAWN ||
              kj < 7 && new_pieces[ki + 1][kj + 1] == Piece.WHITE_PAWN)) {
        return true;
      }
    }

    // check knight positions
    Pos[] knight_diffs = new Pos[]{
            new Pos(-1, -2), new Pos(-2, -1), new Pos(-2, 1), new Pos(-1, 2), new Pos(1, 2), new Pos(2, 1), new Pos(2, -1), new Pos(1, -2)
    };
    for (Pos diff : knight_diffs) {
      int di = diff.x;
      int dj = diff.y;
      int ni = ki + di;
      int nj = kj + dj;
      if (0 <= ni && ni < 8 && 0 <= nj && nj < 8 && new_pieces[ni][nj].is_knight()
              && new_pieces[ni][nj].is_color(opp)) {
        return true;
      }
    }

    // can't be directly next to a king
    for (int di = Math.max(-ki, -1); di < Math.min(8 - ki, 2); di++) {
      for (int dj = Math.max(-kj, -1); dj < Math.min(8 - kj, 2); dj++) {
        if (new_pieces[ki + di][kj + dj].is_king() && new_pieces[ki + di][kj + dj].is_color(opp)) {
          return true;
        }
      }
    }

    // not in check!
    return false;
  }

  public boolean is_win() {
    // black has no moves and is in check
    return get_legal_moves(Color.BLACK).size() == 0 && is_in_check(pieces, Color.BLACK, black_king_pos);
  }

  public boolean is_lose() {
    // white has no moves and is in check
    return get_legal_moves(Color.WHITE).size() == 0 && is_in_check(pieces, Color.WHITE, white_king_pos);
  }

  public boolean is_draw(Color agent) {
    return is_stalemate() || insufficient_material() || is_repetition(agent);
  }

  public boolean is_stalemate() {
    return get_legal_moves(Color.WHITE).size() == 0 && !is_in_check(pieces, Color.WHITE, white_king_pos) ||
            get_legal_moves(Color.BLACK).size() == 0 && !is_in_check(pieces, Color.BLACK, black_king_pos);
  }

  public boolean is_end_state(Color agent) {
    return get_legal_moves(agent).size() == 0 || insufficient_material() || is_repetition(agent);
  }

  public boolean is_repetition(Color agent) {
    return Collections.frequency(last_states, toFenString(agent)) >= 2;
  }

  public boolean insufficient_material() {
    for (Piece[] row : pieces) {
      for (Piece piece : row) {
        if (!piece.is_king() && piece != Piece.EMPTY) {
          return false;
        }
      }
    }
    return true;
  }

  public Piece get_piece_at(Pos loc) {
    return pieces[loc.x][loc.y];
  }

  private double get_material() {
    int score = 0;
    for (Piece[] row : pieces) {
      for (Piece piece : row) {
        score += piece.get_value();
      }
    }
    return score;
  }

  public double evaluate(Color agent) {
    if (is_end_state(agent)) {
      return (is_win() ? 1000 : 0) - (is_lose() ? 1000 : 0);
    }
    return 10 * get_material()
            + 0.5 * castle_eval()
            + 0.2 * piece_activity()
            + 0.1 * pawn_distance()
            + get_endgame_multiplier() * (
            king_activity() * 0.2
                    + pawn_distance() * 0.5
    );
  }

  public void print_evals() {
    System.out.print(" material " + get_material());
    System.out.print(" castle " + castle_eval());
    System.out.print(" piece " + piece_activity());
    System.out.print(" pawn " + pawn_distance());
    System.out.print(" endgame " + get_endgame_multiplier());
    System.out.print(" num " + get_num_pieces());
    System.out.print(" king " + king_activity());
  }

  private double pawn_distance() {
    int total = 0;
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        Piece piece = pieces[i][j];
        if (piece.is_pawn()) {
          if (piece.is_white()) {
            total += (7 - i);
          } else {
            total -= i;
          }
        }
      }
    }
    return total;
  }

  private double king_activity() {
    int wi = white_king_pos.x;
    int wj = white_king_pos.y;
    int bi = black_king_pos.x;
    int bj = black_king_pos.y;
    return -Math.abs(4 - wi) - Math.abs(5 - wj) + Math.abs(4 - bi) + Math.abs(4 - bj);
  }

  private double piece_activity() {
    double total = 0;
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        Piece piece = get_piece_at(new Pos(i, j));
        if (piece.is_knight() || piece.is_bishop()) {
          if (piece.is_white() && i == 7) {
            total -= 1;
          } else if (piece.is_black() && i == 0) {
            total += 1;
          }
        }
      }
    }
    return total;
  }

  private double castle_eval() {
    double total = 0;
    if (whc) {
      total += 1;
      Pos wkp = get_king_pos(Color.WHITE);
      int num_pawns = 0;
      int start = wkp.y < 4 ? 1 : 5;
      int stop = wkp.y < 4 ? 4 : 8;
      for (int j = start; j < stop; j++) {
        Piece p = get_piece_at(new Pos(wkp.x - 1, j));
        if (p.is_pawn() && p.is_white()) {
          num_pawns += 1;
        }
      }
      if (num_pawns < 2) {
        total -= 2;
      }
    }
    // if there are pawns on that side of the board +1, otherwise -1
    if(bhc) {
      total -= 1;
      Pos bkp = get_king_pos(Color.BLACK);
      int num_pawns = 0;
      int start = bkp.y < 4 ? 1 : 5;
      int stop = bkp.y < 4 ? 4 : 8;
      for (int j = start; j < stop; j++) {
        Piece p = get_piece_at(new Pos(bkp.x + 1, j));
        if (p.is_pawn() && p.is_black()) {
          num_pawns += 1;
        }
      }
      if (num_pawns < 2) {
        total += 2;
      }
    }
    return total;
  }

  private double get_endgame_multiplier() {
    return 1 - (get_num_pieces() / 32.0);
  }

  private double get_num_pieces() {
    double total = 0;
    for (Piece[] row : pieces) {
      for (Piece piece : row) {
        if (piece != Piece.EMPTY) {
          total += 1;
        }
      }
    }
    return total;
  }

  public String toFenString(Color agent) {
    StringBuilder result = new StringBuilder();
    for (Piece[] row : pieces) {
      int num_empty = 0;
      for (Piece piece : row) {
        if (piece == Piece.EMPTY) {
          num_empty += 1;
        } else {
          if (num_empty > 0) {
            result.append(num_empty);
            num_empty = 0;
          }
          result.append(piece.get_fen_value());
        }
      }
      if (num_empty > 0) {
        result.append(num_empty);
      }
      result.append("/");
    }
    result.setLength(result.length() - 1);
    result.append(agent == Color.WHITE ? " w " : " b ");
    if (!(wcl && wcr && bcl && bcr)) {
      result.append("-");
    }
    result.append(wcr ? "K" : "");
    result.append(wcl ? "Q" : "");
    result.append(bcr ? "k" : "");
    result.append(bcl ? "q" : "");
    // ******* this should be different but it's unused ******
    result.append(" - 0 1");
    return result.toString();
  }

  public String toString() {
    StringBuilder result = new StringBuilder("-----------------------\n");
    for (Piece[] row : pieces) {
      for (Piece piece : row) {
        result.append(piece);
        result.append("  ");
      }
      result.append("\n");
    }
    result.append("-----------------------");
    return result.toString();
  }

  public static ChessState fromString(String state) {
    state = state.replace("-\n", "");
    state = state.replace("-", "");
//    state = state.strip();
//    System.out.println(state);
    Piece[][] pieces = new Piece[8][8];
    String[] rows = state.split("\n");
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        pieces[i][j] = Piece.fromString(rows[i].charAt(3 * j));
      }
    }
    return new ChessState(pieces);
  }
}
