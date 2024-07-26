import curses


class Display:

    def __init__(self, dimensions: tuple):
        """ Set up a new display via curses

        :param dimensions: A tuple of the form (columns, rows) describing the dimensions of the display
        """
        self.screen = curses.initscr()
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
        index = 0
        for story in stories:
            self.window.move(index * 2, 0)
            story_title = story.source + " " + str(story.datetime)[11:16] + " " + story.title
            if len(story_title) > 78:
                story_title = story_title[:79] + ".."
            story_summary = story.summary
            if len(story_summary) > 78:
                story_summary = story_summary[:78] + ".."
            self.window.addstr(story_title, curses.A_BOLD)
            self.window.move((index * 2) + 1, 0)
            self.window.addstr(story_summary)
            index += 1
        self.window.refresh()
        return

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
