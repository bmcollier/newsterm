import curses

STORY_ROWS = 2

class Display:



    def __init__(self, dimensions: tuple):
        """ Set up a new display via curses

        :param dimensions: A tuple of the form (columns, rows) describing the dimensions of the display
        """
        self.screen = curses.initscr()
        self.dimensions = dimensions
        curses.noecho()
        curses.cbreak()
        self.screen.nodelay(True)
        self.screen.keypad(True)
        self.window = curses.newwin(dimensions[1], dimensions[0], 0, 0)

    def update(self, stories: list):
        """Write stories to display

        :param stories: Set of stories to display
        :return:
        """
        self.window.clear()
        self.write_top_story(stories[0], 6)
        index = 0
        for story in stories[1:]:
            self.window.move((index * STORY_ROWS)+6, 0)
            self.write_story_lines(story, (index * STORY_ROWS)+6)
            index += 1
        self.window.refresh()
        return

    def write_top_story(self, story, lines):
        top_line = f"Newsterm | Latest story: {story.source} ({str(story.datetime)[11:16]})"
        recency_line = f"Retrieved at {str(story.retrieved)[11:16]} 1/1"
        top_line = top_line + (" " * ((self.dimensions[0] - len(recency_line)) - (len(top_line))))
        title_line = story.title
        summary_line = story.summary

        if len(top_line) > self.dimensions[0] - len(recency_line):
            top_line = top_line[:self.dimensions[0] - 20] + ".."

        if len(title_line) > self.dimensions[0]:
            title_line = title_line[:self.dimensions[0] - 2] + ".."

        if len(summary_line) > self.dimensions[0] * 3:
            summary_line = summary_line[:(self.dimensions[0] * 3) - 2] + ".."

        top_line += recency_line

        self.window.move(0, 0)
        self.window.addstr(top_line[0:self.dimensions[0]-7], curses.A_REVERSE)
        self.window.addstr(":", curses.A_REVERSE + curses.A_BLINK)
        self.window.addstr(top_line[self.dimensions[0]-6:], curses.A_REVERSE)

        self.window.move(1, 0)
        self.window.addstr(title_line, curses.A_BOLD)
        self.window.move(2, 0)
        self.window.addstr(summary_line, curses.A_NORMAL)

    def write_story_lines(self, story, start_row):
        title_line = f"{str(story.datetime)[11:16]} {story.source} {story.title}"
        summary_line = story.summary

        if len(title_line) > self.dimensions[0]:
            title_line = title_line[:self.dimensions[0]-2] + ".."

        if len(summary_line) > self.dimensions[0]:
            summary_line = summary_line[:self.dimensions[0]-2] + ".."

        self.window.addstr(title_line, curses.A_BOLD)
        self.window.move(start_row + 1, 0)
        self.window.addstr(summary_line, curses.A_NORMAL)

    def quit_requested(self):
        """ Check if the user has pressed the Q key to quit the application.

        :return: True if q has been pressed, False otherwise
        """
        key = self.screen.getch()
        if key == -1:
            return False
        elif key == ord('q'):
            return True
        else:
            return False

    def clean_quit(self):
        """ Restore the terminal to a normal state

        :return: None
        """
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
