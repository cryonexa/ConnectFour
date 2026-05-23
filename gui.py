import pygame

ROWS = 6
COLS = 7
CELL = 100
RADIUS = 42

WIDTH = COLS * CELL
BOARD_HEIGHT = (ROWS + 1) * CELL  # +1 row for the hover area at top
MENU_HEIGHT = 400

C_BG = (15, 15, 25)
C_BOARD = (30, 80, 180)
C_EMPTY = (20, 20, 35)
C_P1 = (220, 60, 60)
C_P2 = (240, 200, 40)
C_TEXT = (230, 230, 230)
C_BTN = (50, 50, 80)
C_BTN_HOVER = (80, 80, 130)

PLAYER_COLORS = {1: C_P1, 2: C_P2}


def _font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui", size, bold=True)


# ---------------------------------------------------------------------------
# Menu screen
# ---------------------------------------------------------------------------

def draw_menu(screen: pygame.Surface) -> None:
    screen.fill(C_BG)
    title = _font(56).render("Connect Four", True, C_TEXT)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

    mx, my = pygame.mouse.get_pos()
    for i, label in enumerate(["2 Player", "vs AI"]):
        rect = pygame.Rect(WIDTH // 2 - 130, 210 + i * 100, 260, 60)
        color = C_BTN_HOVER if rect.collidepoint(mx, my) else C_BTN
        pygame.draw.rect(screen, color, rect, border_radius=12)
        text = _font(30).render(label, True, C_TEXT)
        screen.blit(text, text.get_rect(center=rect.center))


def menu_button_at(pos: tuple[int, int]) -> str | None:
    """Return 'two_player' | 'ai' | None depending on which button was clicked."""
    x, y = pos
    for i, mode in enumerate(["two_player", "ai"]):
        rect = pygame.Rect(WIDTH // 2 - 130, 210 + i * 100, 260, 60)
        if rect.collidepoint(x, y):
            return mode
    return None


# ---------------------------------------------------------------------------
# In-game rendering
# ---------------------------------------------------------------------------

def draw_board(screen: pygame.Surface, grid: list[list[int]]) -> None:
    pygame.draw.rect(screen, C_BOARD, (0, CELL, WIDTH, ROWS * CELL))
    for r in range(ROWS):
        for c in range(COLS):
            player = grid[r][c]
            color = PLAYER_COLORS.get(player, C_EMPTY)
            cx = c * CELL + CELL // 2
            cy = (r + 1) * CELL + CELL // 2  # +1 for hover row
            pygame.draw.circle(screen, color, (cx, cy), RADIUS)


def draw_hover(screen: pygame.Surface, col: int, player: int) -> None:
    if col < 0:
        return
    cx = col * CELL + CELL // 2
    cy = CELL // 2
    pygame.draw.circle(screen, PLAYER_COLORS[player], (cx, cy), RADIUS)


def draw_status(screen: pygame.Surface, text: str, color: tuple = C_TEXT) -> None:
    surf = _font(26).render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, CELL // 2)))


def draw_result_banner(screen: pygame.Surface, text: str) -> None:
    overlay = pygame.Surface((WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    msg = _font(48).render(text, True, C_TEXT)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, BOARD_HEIGHT // 2 - 20)))
    sub = _font(22).render("Click anywhere to continue", True, (180, 180, 180))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, BOARD_HEIGHT // 2 + 40)))


def col_from_x(x: int) -> int:
    return x // CELL
