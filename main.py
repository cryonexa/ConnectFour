import sys
import pygame

from board import Board
from ai import AI
from gui import (
    WIDTH, BOARD_HEIGHT,
    draw_menu, menu_button_at,
    draw_board, draw_hover, draw_status, draw_result_banner,
    col_from_x,
)

PLAYER_NAMES = {1: "Red", 2: "Yellow"}
FPS = 60


def run_game(screen: pygame.Surface, clock: pygame.time.Clock, vs_ai: bool) -> None:
    board = Board()
    ai = AI() if vs_ai else None
    current = 1          # 1 = P1 (Red), 2 = P2/AI (Yellow)
    hover_col = -1
    game_over = False
    result_text = ""

    screen = pygame.display.set_mode((WIDTH, BOARD_HEIGHT))

    while True:
        clock.tick(FPS)
        screen.fill((15, 15, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return  # back to menu
                continue

            # Human turn only for mouse events
            is_human_turn = not vs_ai or current == 1

            if event.type == pygame.MOUSEMOTION and is_human_turn:
                hover_col = col_from_x(event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and is_human_turn:
                col = col_from_x(event.pos[0])
                if board.is_valid(col):
                    board.drop(col, current)
                    if board.check_win(current):
                        game_over = True
                        result_text = f"{PLAYER_NAMES[current]} wins!"
                    elif board.is_draw():
                        game_over = True
                        result_text = "It's a draw!"
                    else:
                        current = 3 - current  # toggle 1 <-> 2

        # AI turn (runs outside the event loop so it happens once per frame)
        if not game_over and vs_ai and current == 2:
            hover_col = -1
            pygame.time.wait(300)
            col = ai.get_move(board)
            board.drop(col, current)
            if board.check_win(current):
                game_over = True
                result_text = "AI wins!"
            elif board.is_draw():
                game_over = True
                result_text = "It's a draw!"
            else:
                current = 1

        draw_board(screen, board.grid)

        if not game_over:
            if not (vs_ai and current == 2):
                draw_hover(screen, hover_col, current)
            label = "AI is thinking..." if vs_ai and current == 2 else f"{PLAYER_NAMES[current]}'s turn"
            draw_status(screen, label)
        else:
            draw_result_banner(screen, result_text)

        pygame.display.flip()


def run_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> bool | None:
    """Returns True for AI mode, False for 2-player, None to quit."""
    screen = pygame.display.set_mode((WIDTH, 400))
    while True:
        clock.tick(FPS)
        draw_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode = menu_button_at(event.pos)
                if mode == "two_player":
                    return False
                if mode == "ai":
                    return True


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Connect Four")
    screen = pygame.display.set_mode((WIDTH, 400))
    clock = pygame.time.Clock()

    while True:
        choice = run_menu(screen, clock)
        if choice is None:
            break
        run_game(screen, clock, vs_ai=choice)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
