import curses
from collections import OrderedDict


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
            self.window.addstr(content.source + " " + content.published[17:22] + " " + content.get("title"), curses.A_BOLD)
            self.window.move((index * 2) + 1, 0)
            self.window.addstr(content.summary)
        self.window.refresh()


