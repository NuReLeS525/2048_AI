# mcts_2048_run.py
import sys
import os
sys.path.append(os.getcwd())   # IMPORTANT: parentheses
from game_defs_2048 import Board
import copy
import numpy as np
from random import randint, choice
from tkinter import *
from PIL import Image, ImageTk
import time

OPTIONS = ['up', 'down', 'left', 'right']

def mcts_choose_move(board, trials=300, depth=10):
    """
    Simple Monte Carlo: for each possible first move, run many random playouts and
    take the move with highest average final score.
    """
    # generate list of legal first moves (those that change the board)
    legal_moves = []
    for move in OPTIONS:
        bcopy = copy.deepcopy(board)
        changed, _ = bcopy.move(move)
        if changed:
            legal_moves.append(move)

    if not legal_moves:
        return None

    avg_scores = {m: [] for m in legal_moves}

    for m in legal_moves:
        for t in range(trials // len(legal_moves)):
            btest = copy.deepcopy(board)
            # perform the first chosen move
            btest.move(m)
            # simulate random plays for 'depth' moves
            for d in range(depth):
                if btest.over:
                    break
                # pick a random valid move
                possible = []
                for mv in OPTIONS:
                    btmp = copy.deepcopy(btest)
                    ch, _ = btmp.move(mv)
                    if ch:
                        possible.append(mv)
                if not possible:
                    break
                btest.move(choice(possible))
            avg_scores[m].append(btest.score)
    # compute means
    means = {m: (np.mean(avg_scores[m]) if avg_scores[m] else -1) for m in avg_scores}
    # pick best
    best_move = max(means, key=lambda k: means[k])
    return best_move

# ---- GUI helpers ----
class GUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        root.title("2048 - AI")
        root.geometry("654x608")
        # try background.png
        try:
            self.img = ImageTk.PhotoImage(Image.open("background.png"))
            self.bg = Label(root, image=self.img)
            self.bg.place(x=0, y=0)
        except Exception:
            self.root.configure(bg="#bbada0")

        self.score_label = Label(root, text=str(board.score), font=("Helvetica", 26))
        self.score_label.place(x=225, y=88)

        # create 4x4 label grid (we will update text)
        self.cells = []
        xs = [108, 228, 348, 468]
        ys = [185, 280, 380, 480]
        for i in range(4):
            row = []
            for j in range(4):
                lbl = Label(root, text="", font=("Helvetica", 26), width=4, height=1)
                lbl.place(x=xs[j], y=ys[i])
                row.append(lbl)
            self.cells.append(row)
        root.update()

    def update(self):
        state = self.board.as_numpy()
        self.score_label.config(text=str(self.board.score))
        for i in range(4):
            for j in range(4):
                val = int(state[i, j])
                lbl = self.cells[i][j]
                if val > 0:
                    lbl.config(text=str(val))
                else:
                    lbl.config(text="")

        self.root.update()

def run_game(trials=300, depth=10, delay=0.05):
    b = Board()
    root = Tk()
    gui = GUI(root, b)
    # run until over
    while not b.over:
        gui.update()
        # choose move with MCTS
        move = mcts_choose_move(b, trials=trials, depth=depth)
        if not move:
            break
        b.move(move)
        time.sleep(delay)
        root.update()
    gui.update()
    print("Game finished. Score:", b.score)
    root.mainloop()   # keep window open when done

if __name__ == "__main__":
    # you can change trials/depth to make AI slower/stronger
    run_game(trials=300, depth=8, delay=0.02)
