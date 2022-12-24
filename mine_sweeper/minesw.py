from pickle import APPEND
import random
import enum
from copy import deepcopy

class tileType(enum.IntEnum):
    Empty = 0
    Bomb = -1
    Flag = -2
    Unknown = -3

class MinerField:
    def __init__(self, rows : int, cols : int):
        self.rows = rows
        self.cols = cols
        self.field = [ [0]*cols for _ in range(rows) ]
        self.user_view = [ [-3]*cols for _ in range(rows) ]

    def get_line(self, r : int, hidden : bool = True):
        if (r >= self.rows or r < 0):
            return None
        return self.field[r] if hidden else self.field[r]

    def set_flag(self, r : int, c : int):
        if self.user_view[r][c] == tileType.Flag:
            self.user_view[r][c] = tileType.Unknown
        elif self.user_view[r][c] == tileType.Unknown:
            self.user_view[r][c] = tileType.Flag

    def is_in_range(self, r, c) -> bool:
        return r >= 0 and r < self.rows and c >= 0 and c < self.cols

    def _open_neigh_empties(self, r : int, c : int):
        queue = []
        queue.append((r, c))
        self.user_view[r][c] = self.field[r][c]

        while queue:
            rr, cc = queue.pop()
            for i, j in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                if (self.is_in_range(rr+i, cc+j) and self.user_view[rr+i][cc+j] == tileType.Unknown):
                    self.user_view[rr+i][cc+j] = self.field[rr+i][cc+j]
                    if (self.field[rr+i][cc+j] == tileType.Empty):
                        queue.append((rr+i, cc+j))

    def open_tile(self, r : int, c : int) -> bool:
        if (self.user_view[r][c] == tileType.Unknown):
            if (self.field[r][c] == tileType.Bomb):
                return False
            elif (self.field[r][c] == tileType.Empty):
                self._open_neigh_empties(r, c)
            else:
                self.user_view[r][c] = self.field[r][c]
        return True

    def __add_nearby(self, r, c):
        for i, j in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            if self.is_in_range(r+i,c+j) and self.field[r+i][c+j] != -1:
                self.field[r+i][c+j] += 1

    def generate_bomb(self, count:int):
        bombs = random.choices(range(self.rows*self.cols), k=count)
        for xy in bombs:
            bomb_r, bomb_c = xy // self.cols, xy % self.cols
            self.field[bomb_r][bomb_c] = -1
            self.__add_nearby(bomb_r, bomb_c)

