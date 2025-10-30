# game_defs_2048.py
import random
import numpy as np

class Board:
    def __init__(self, n=4):
        self.n = n
        self.state = [[0]*n for _ in range(n)]
        self.score = 0
        self.over = False
        self.win = False
        # start: add two tiles
        self._add_random_tile()
        self._add_random_tile()

    def get_empty_cells(self):
        empties = []
        for i in range(self.n):
            for j in range(self.n):
                if self.state[i][j] == 0:
                    empties.append((i, j))
        return empties

    def _add_random_tile(self):
        empties = self.get_empty_cells()
        if not empties:
            return False
        i, j = random.choice(empties)
        self.state[i][j] = 4 if random.random() > 0.9 else 2
        return True

    def _compress_and_merge_row(self, row):
        """Compress a row to the left and merge equal tiles.
           Returns new_row, gained_score."""
        new = [v for v in row if v != 0]
        gained = 0
        i = 0
        merged = []
        while i < len(new):
            if i+1 < len(new) and new[i] == new[i+1]:
                val = new[i]*2
                merged.append(val)
                gained += val
                i += 2
            else:
                merged.append(new[i])
                i += 1
        merged += [0] * (self.n - len(merged))
        return merged, gained

    def _transpose(self):
        self.state = [list(row) for row in zip(*self.state)]

    def _reverse_rows(self):
        self.state = [list(reversed(row)) for row in self.state]

    def move(self, direction):
        """Perform move. Returns True if the board changed, and score gained."""
        before = [row[:] for row in self.state]
        gained_total = 0

        if direction == 'up':
            self._transpose()
            for i in range(self.n):
                newrow, gained = self._compress_and_merge_row(self.state[i])
                self.state[i] = newrow
                gained_total += gained
            self._transpose()

        elif direction == 'down':
            self._transpose()
            self._reverse_rows()
            for i in range(self.n):
                newrow, gained = self._compress_and_merge_row(self.state[i])
                self.state[i] = newrow
                gained_total += gained
            self._reverse_rows()
            self._transpose()

        elif direction == 'left':
            for i in range(self.n):
                newrow, gained = self._compress_and_merge_row(self.state[i])
                self.state[i] = newrow
                gained_total += gained

        elif direction == 'right':
            self._reverse_rows()
            for i in range(self.n):
                newrow, gained = self._compress_and_merge_row(self.state[i])
                self.state[i] = newrow
                gained_total += gained
            self._reverse_rows()
        else:
            raise ValueError("direction must be one of 'up', 'down', 'left', 'right'")

        changed = (before != self.state)
        if changed:
            self.score += gained_total
            self._add_random_tile()

        # update state flags
        self._update_game_state()
        return changed, gained_total

    def _update_game_state(self):
        # check win
        for i in range(self.n):
            for j in range(self.n):
                if self.state[i][j] == 2048:
                    self.win = True

        # if there is any empty cell -> not over
        if any(0 in row for row in self.state):
            self.over = False
            return

        # check if any merge possible
        for i in range(self.n):
            for j in range(self.n-1):
                if self.state[i][j] == self.state[i][j+1]:
                    self.over = False
                    return
        for j in range(self.n):
            for i in range(self.n-1):
                if self.state[i][j] == self.state[i+1][j]:
                    self.over = False
                    return

        # otherwise over
        self.over = True

    def as_numpy(self):
        return np.array(self.state)
