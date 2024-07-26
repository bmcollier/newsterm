import curses
import unittest

from unittest.mock import patch, MagicMock

from newsterm.display import Display


class TestDisplay(unittest.TestCase):

    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.endwin')
    @patch('curses.newwin')
    @patch('curses.nocbreak')
    @patch('curses.echo')
    def setUp(self, mock_echo, mock_nocbreak, mock_newwin, mock_endwin, mock_cbreak, mock_noecho, mock_initscr):

        self.mock_screen = MagicMock()
        mock_initscr.return_value = self.mock_screen
        self.mock_window = MagicMock()
        mock_newwin.return_value = self.mock_window

        self.display = Display((80, 24))

    def test_update(self):
        stories = [
            MagicMock(source='Source1', datetime='2024-07-25 12:34:55', title='Title1', summary='Summary1'),
            MagicMock(source='Source2', datetime='2024-07-25 13:34:56', title='Title2', summary='Summary2')
        ]

        self.display.update(stories)

        self.mock_window.clear.assert_called_once()
        self.mock_window.refresh.assert_called_once()
        self.mock_window.addstr.assert_any_call('Source1 12:34 Title1', curses.A_BOLD)
        self.mock_window.addstr.assert_any_call('Summary1')
        self.mock_window.addstr.assert_any_call('Source2 13:34 Title2', curses.A_BOLD)
        self.mock_window.addstr.assert_any_call('Summary2')

    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.endwin')
    @patch('curses.newwin')
    def test_quit_requested(self, mock_newwin, mock_endwin, mock_cbreak, mock_noecho, mock_initscr):
        mock_screen = MagicMock()
        mock_initscr.return_value = mock_screen
        mock_screen.getch.side_effect = [ord('q')]
        display = Display((80, 24))
        self.assertTrue(display.quit_requested())

    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.endwin')
    @patch('curses.newwin')
    @patch('curses.nocbreak')
    @patch('curses.echo')
    def test_clean_quit(self, mock_echo, mock_nocbreak, mock_newwin, mock_endwin, mock_cbreak, mock_noecho,
                        mock_initscr):
        self.mock_screen = MagicMock()
        mock_initscr.return_value = self.mock_screen
        self.mock_window = MagicMock()
        mock_newwin.return_value = self.mock_window
        display = Display((80, 24))
        self.mock_screen.keypad.reset_mock()
        display.clean_quit()
        self.mock_screen.keypad.assert_called_once_with(False)
        mock_echo.assert_called_once()
        mock_nocbreak.assert_called_once()
        mock_endwin.assert_called_once()
