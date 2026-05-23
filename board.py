ROWS = 6
COLS = 7

EMPTY = 0


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]

    def is_valid(self, col: int) -> bool:
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def get_valid_cols(self) -> list[int]:
        return [c for c in range(COLS) if self.is_valid(c)]

    def drop(self, col: int, player: int) -> int:
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = player
                return row
        raise ValueError(f"Column {col} is full")

    def check_win(self, player: int) -> bool:
        g = self.grid
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(g[r][c + i] == player for i in range(4)):
                    return True
        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(g[r + i][c] == player for i in range(4)):
                    return True
        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(g[r + i][c + i] == player for i in range(4)):
                    return True
        # Diagonal down-left
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if all(g[r + i][c - i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self) -> bool:
        return all(self.grid[0][c] != EMPTY for c in range(COLS))

    def copy(self) -> "Board":
        b = Board()
        b.grid = [row[:] for row in self.grid]
        return b
