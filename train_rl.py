"""
Connect Four — Deep Q-Network training
=======================================
Trains an agent via self-play and saves the weights to model.pth.
Once model.pth exists the Pygame game (main.py) will load it automatically.

Requirements:
    pip install torch numpy

Usage:
    python train_rl.py
"""

import random
from collections import deque
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

from ai import DQN, MODEL_PATH


# ---------------------------------------------------------------------------
# Game environment (self-contained — mirrors Board logic without Pygame dep)
# ---------------------------------------------------------------------------

class ConnectFourEnv:
    ROWS, COLS = 6, 7

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1

    def reset(self):
        self.board[:] = 0
        self.current_player = 1
        return self._state()

    def _state(self):
        return self.board.flatten().astype(float)

    def valid_actions(self):
        return [c for c in range(self.COLS) if self.board[0][c] == 0]

    def drop(self, col, player):
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return

    def _check_win(self, player):
        b = self.board
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if all(b[r][c + i] == player for i in range(4)):
                    return True
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if all(b[r + i][c] == player for i in range(4)):
                    return True
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if all(b[r + i][c + i] == player for i in range(4)):
                    return True
        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                if all(b[r - i][c + i] == player for i in range(4)):
                    return True
        return False

    def step(self, action):
        if action not in self.valid_actions():
            return self._state(), -1.0, True

        self.drop(action, self.current_player)

        if self._check_win(self.current_player):
            return self._state(), 1.0, True
        if not self.valid_actions():
            return self._state(), 0.5, True

        self.current_player = 3 - self.current_player
        return self._state(), 0.0, False


# ---------------------------------------------------------------------------
# DQN Agent
# ---------------------------------------------------------------------------

class DQNAgent:
    def __init__(self):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()
        self.memory = deque(maxlen=10_000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

    def act(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        with torch.no_grad():
            q = self.model(torch.FloatTensor(state).unsqueeze(0)).squeeze().numpy()
        return max(valid_actions, key=lambda a: float(q[a]))

    def remember(self, *experience):
        self.memory.append(experience)

    def train_step(self, batch_size=64):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            s = torch.FloatTensor(state)
            ns = torch.FloatTensor(next_state)
            target = reward
            if not done:
                with torch.no_grad():
                    target += self.gamma * self.model(ns).max().item()
            q = self.model(s)
            tq = q.clone().detach()
            tq[action] = target
            loss = self.loss_fn(q, tq)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train(episodes: int = 3000) -> DQNAgent:
    env = ConnectFourEnv()
    agent = DQNAgent()

    recent_results: deque[str] = deque(maxlen=100)  # 'W', 'D', 'L'

    bar = tqdm(range(1, episodes + 1), desc="Training", unit="ep", ncols=80)
    try:
        for ep in bar:
            state = env.reset()
            done = False
            result = "L"
            while not done:
                action = agent.act(state, env.valid_actions())
                next_state, reward, done = env.step(action)
                agent.remember(state, action, reward, next_state, done)
                agent.train_step()
                state = next_state
                if done:
                    if reward == 1.0:
                        result = "W"
                    elif reward == 0.5:
                        result = "D"

            recent_results.append(result)

            if ep % 50 == 0:
                wins  = recent_results.count("W")
                draws = recent_results.count("D")
                bar.set_postfix(
                    eps=f"{agent.epsilon:.2f}",
                    win=f"{wins}%",
                    draw=f"{draws}%",
                )

            if ep % 200 == 0:
                torch.save(agent.model.state_dict(), MODEL_PATH)

    except KeyboardInterrupt:
        print("\nInterrupted — saving current weights...")

    torch.save(agent.model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print("Launch main.py — the AI will now use the trained model.\n")
    return agent


if __name__ == "__main__":
    train(episodes=3000)
