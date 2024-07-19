import curses
import pytz
from collections import OrderedDict
from datetime import datetime, timedelta


class Display:

    def __init__(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.window = curses.newwin(25, 80, 0, 0)
        # self.window.move(0, 0)
        # self.window.addstr("Initialising")
        # self.window.refresh()

    def update(self, stories: OrderedDict):
        self.window.clear()
        for index, content in stories.items():
            self.window.move(index * 2, 0)

            published_dt = datetime.strptime(content.published, "%a, %d %b %Y %H:%M:%S %Z")
            published_dt_local = published_dt + timedelta(hours=1)

            self.window.addstr(content.source + " " + str(published_dt_local)[11:16] + " " + content.get("title"), curses.A_BOLD)
            self.window.move((index * 2) + 1, 0)
            self.window.addstr(content.summary)
        self.window.refresh()


