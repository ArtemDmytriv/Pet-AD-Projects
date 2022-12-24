from sre_constants import CHARSET
from typing import Dict
from minesw import MinerField, tileType
import curses

default_m_chars = { tileType.Bomb : "#",
        tileType.Flag : "F",
        tileType.Empty : " ",
        tileType.Unknown : "·"
        }

class cliMinerField (MinerField):
    def __init__(self, rows : int, cols : int, map_chars : Dict[int, str]):
        MinerField.__init__(self, rows, cols)
        self.map_chars = self.validated_map_chars(map_chars)

    def validated_map_chars(self, m_chars : Dict[int, str]):
        for val in filter(lambda x : x not in m_chars.keys(), tileType):
            m_chars[val] = default_m_chars[val]

        for num in filter(lambda x : x not in m_chars.keys(), range(1, 9)):
            m_chars[num] = str(num)
        return m_chars

    def get_str_line(self, row : int, hidden : bool = True):
        if not self.is_in_range(row, 0):
            raise ValueError(f"Wrong row number, must be < {self.rows}")
        f = self.user_view if hidden else self.field
        return "".join(map(lambda x : "{:3}".format(self.map_chars[x]), f[row]))

    def print_field(self, hidden : bool = True):
        for row in range(self.rows):
            print(self.get_str_line(row, hidden))


def draw_field(screen, mf, hidden : bool = True):
    for row in range(mf.rows):
        line = mf.get_str_line(row, hidden)
        try:
            screen.addstr(row, 0, line);
        except curses.error:
            pass

def gen_map_chars():
    num_char_m = { i : str(i) for i in range(1,10) }
    num_char_m[tileType.Empty] = " "
    num_char_m[tileType.Bomb] = ""
    num_char_m[tileType.Flag] = ""
    num_char_m[tileType.Unknown] = "·"
    return num_char_m

def main(screen):
    # init curses
    screen.keypad(1)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.flushinp()
    curses.noecho()
    screen.clear()

    #if curses.can_change_color():
    #    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    #init minesw field
    max_y, max_x = screen.getmaxyx()

    r = max_y
    c = max_x // 3
    mf = cliMinerField(r, c, gen_map_chars())
    mf.generate_bomb(r*c // 10)

    draw_field(screen, mf, True)
    while True:
        key = screen.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, button = curses.getmouse()
            # LMB was clicked
            if button == 4:
                if (mf.open_tile(y, (x+1) // 3) == False):
                    screen.clear()
                    draw_field(screen, mf, False)
                    key = screen.getch()
                    break

            # RMB was clicked
            if button == 4096:
                mf.set_flag(y, (x+1) // 3)

        draw_field(screen, mf, True)

curses.wrapper(main)
