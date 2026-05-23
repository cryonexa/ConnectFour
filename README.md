# Connect Four

A Python implementation of the classic **Connect Four** board game, supporting both a terminal interface and a Pygame graphical interface, with a built-in AI opponent.

## Gameplay

Connect Four is a two-player strategy game played on a 6×7 grid. Players take turns dropping colored discs into columns. The first player to connect four of their discs in a row — horizontally, vertically, or diagonally — wins.

## Features

- **Terminal mode** — play directly in the console with a text-based board
- **Pygame GUI mode** — graphical window with colored discs and smooth interaction
- **AI opponent** — single-player mode with a CPU challenger
- **Local multiplayer** — two players on the same machine

## Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) (for GUI mode)

## Installation

```bash
git clone https://github.com/cryonexa/ConnectFour.git
cd ConnectFour
pip install pygame
```

## Running the Game

**Terminal mode:**
```bash
python main.py --mode terminal
```

**GUI mode:**
```bash
python main.py --mode gui
```

## How to Play

1. Players alternate turns.
2. On your turn, choose a column (1–7) to drop your disc.
3. The disc falls to the lowest available row in that column.
4. First to align **four discs** in any direction wins.
5. If the board fills with no winner, the game ends in a draw.

## Project Structure

```
ConnectFour/
├── main.py        # Entry point
├── board.py       # Board logic and win detection
├── ai.py          # AI opponent logic
├── gui.py         # Pygame graphical interface
└── terminal.py    # Terminal interface
```

## License

MIT License — see [LICENSE](LICENSE) for details.
