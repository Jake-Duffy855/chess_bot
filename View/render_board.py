import time

import pygame
from time import sleep
import random
from Game.ChessState import *
from Game.Piece import *
from Search.SearchAgent import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WHITE_SQUARE = (238, 238, 210)
GREEN_SQUARE = (118, 151, 87)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH

SQUARE_SIZE = SCREEN_HEIGHT // 8

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

background = pygame.Surface(screen.get_size())
ts, w, h, c1, c2 = SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE_SQUARE, GREEN_SQUARE
tiles = [((x * ts, y * ts, ts, ts), c1 if (x + y) % 2 == 0 else c2) for x in range((w + ts - 1) // ts) for y in
         range((h + ts - 1) // ts)]
[pygame.draw.rect(background, color, rect) for rect, color in tiles]
screen.blit(background, (0, 0))

chess_state = ChessState(DEFAULT_BOARD)
search_agent = AlphaBetaAgent(2)
auto_move = False
player = Color.WHITE

image_file_by_piece = {
    Piece.WHITE_PAWN: "./pieces_images/white_pawn.png",
    Piece.WHITE_KNIGHT: "./pieces_images/white_knight.png",
    Piece.WHITE_BISHOP: "./pieces_images/white_bishop.png",
    Piece.WHITE_ROOK: "./pieces_images/white_rook.png",
    Piece.WHITE_QUEEN: "./pieces_images/white_queen.png",
    Piece.WHITE_KING: "./pieces_images/white_king.png",
    Piece.BLACK_PAWN: "./pieces_images/black_pawn.png",
    Piece.BLACK_KNIGHT: "./pieces_images/black_knight.png",
    Piece.BLACK_BISHOP: "./pieces_images/black_bishop.png",
    Piece.BLACK_ROOK: "./pieces_images/black_rook.png",
    Piece.BLACK_QUEEN: "./pieces_images/black_queen.png",
    Piece.BLACK_KING: "./pieces_images/black_king.png",
}


rects = []
pieces = []

for i in range(8):
    for j in range(8):
        if chess_state.get_piece_at((i, j)) != Piece.EMPTY:
            rects.append(
                pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pieces.append(
                pygame.transform.smoothscale(
                    pygame.image.load(image_file_by_piece[chess_state.get_piece_at((i, j))]),
                    (SQUARE_SIZE, SQUARE_SIZE))
            )

selected = None
start_square = None
end_square = None
legal_moves = []
random.seed(256)

# --- mainloop ---

clock = pygame.time.Clock()
is_running = True

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, r in enumerate(rects):
                    if r.collidepoint(event.pos):
                        selected = i
                        selected_offset_x = r.x - event.pos[0]
                        selected_offset_y = r.y - event.pos[1]
                        start_square = (
                            event.pos[1] // SQUARE_SIZE,
                            event.pos[0] // SQUARE_SIZE
                        )
                        legal_moves = [m for m in chess_state.get_legal_moves(player) if m.start_pos == start_square]

        elif event.type == pygame.MOUSEBUTTONUP:
            end_square = (
                event.pos[1] // SQUARE_SIZE,
                event.pos[0] // SQUARE_SIZE
            )
            if event.button == 1 and selected is not None:
                legal_moves = []
                move = Action(start_square, end_square)
                if move in chess_state.get_legal_moves(player):
                    chess_state = chess_state.get_successor_state(move, player)
                    print(chess_state)
                    print(move)
                    rects = []
                    pieces = []
                    for i in range(8):
                        for j in range(8):
                            if chess_state.get_piece_at((i, j)) != Piece.EMPTY:
                                rects.append(
                                    pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                                )
                                pieces.append(
                                    pygame.transform.smoothscale(
                                        pygame.image.load(image_file_by_piece[chess_state.get_piece_at((i, j))]),
                                        (SQUARE_SIZE, SQUARE_SIZE))
                                )
                    player = player.get_opposite()
                else:
                    # print(move, [str(m) for m in chess_state.get_legal_moves(player) if
                    #              m.start_pos == start_square])
                    print(move, chess_state.get_legal_moves(player))
                    rects[selected].x = start_square[1] * SQUARE_SIZE
                    rects[selected].y = start_square[0] * SQUARE_SIZE
                start_square = None
                end_square = None
                selected = None

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:  # selected can be `0` so `is not None` is required
                # move object
                rects[selected].x = event.pos[0] + selected_offset_x
                rects[selected].y = event.pos[1] + selected_offset_y

    # draw rect
    screen.blit(background, (0, 0))
    for a in legal_moves:
        i, j = a.end_pos
        pygame.draw.rect(
            screen, (200, 40, 40, 250), pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        )
    for i, r in enumerate(rects):
        screen.blit(pieces[i], r)

    # pygame.display.flip()
    pygame.display.update()

    if chess_state.is_end_state(player):
        continue

    clock.tick(60)
    # sleep(0.5)
    if auto_move:
        best_move = search_agent.get_action(chess_state, player)
        chess_state = chess_state.get_successor_state(best_move, player)
        player = player.get_opposite()
    rects = []
    pieces = []
    for i in range(8):
        for j in range(8):
            if chess_state.get_piece_at((i, j)) != Piece.EMPTY:
                rects.append(
                    pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )
                pieces.append(
                    pygame.transform.smoothscale(
                        pygame.image.load(image_file_by_piece[chess_state.get_piece_at((i, j))]),
                        (SQUARE_SIZE, SQUARE_SIZE))
                )

pygame.quit()
print(chess_state.is_win(), chess_state.is_lose(), chess_state.is_draw())
