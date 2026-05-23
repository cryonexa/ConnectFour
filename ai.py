import random
from pathlib import Path

from board import Board

MODEL_PATH = Path(__file__).parent / "model.pth"


# ---------------------------------------------------------------------------
# Network architecture — shared by ai.py (inference) and train_rl.py (training)
# ---------------------------------------------------------------------------

try:
    import torch
    import torch.nn as nn
    import numpy as np

    class DQN(nn.Module):
        def __init__(self, input_size: int = 42, output_size: int = 7):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(input_size, 128),
                nn.ReLU(),
                nn.Linear(128, 128),
                nn.ReLU(),
                nn.Linear(128, output_size),
            )

        def forward(self, x):
            return self.network(x)

    _TORCH_AVAILABLE = True

except ImportError:
    _TORCH_AVAILABLE = False
    DQN = None  # type: ignore


# ---------------------------------------------------------------------------
# AI wrapper — used by the Pygame game loop
# ---------------------------------------------------------------------------

class AI:
    """AI opponent.

    Loads a trained DQN from model.pth when present and reloads it
    automatically whenever training saves a new checkpoint — so you
    can play while training runs in a second terminal.
    Falls back to random moves when no model file exists yet.
    """

    def __init__(self):
        self.model = None
        self._mtime: float = 0.0
        self._try_load()

    def _try_load(self) -> None:
        if not (_TORCH_AVAILABLE and MODEL_PATH.exists()):
            return
        try:
            mtime = MODEL_PATH.stat().st_mtime
            m = DQN()
            m.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
            m.eval()
            self.model = m
            self._mtime = mtime
            print(f"[AI] Loaded model.pth (mtime={mtime:.0f})")
        except Exception as exc:
            print(f"[AI] Could not load model.pth: {exc} — keeping previous model")

    def _reload_if_updated(self) -> None:
        if not (_TORCH_AVAILABLE and MODEL_PATH.exists()):
            return
        try:
            if MODEL_PATH.stat().st_mtime != self._mtime:
                self._try_load()
        except OSError:
            pass  # file being written — skip this check

    @property
    def using_model(self) -> bool:
        return self.model is not None

    def get_move(self, board: Board) -> int:
        self._reload_if_updated()
        valid = board.get_valid_cols()

        if self.model is None:
            return random.choice(valid)

        state = torch.FloatTensor(
            [cell for row in board.grid for cell in row]
        ).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state).squeeze().numpy()
        return max(valid, key=lambda a: float(q_values[a]))
