import argparse
from pytz import timezone

from newsterm.terminal import Terminal
from newsterm.utils import get_sources

DESCRIPTION = """
Newsterm runs in a terminal window, and works well on a VT100 terminal. The
size of the window can be configured, as can the delay between RSS calls. The
config file takes the following JSON format:

{
  "sources": {
    "Source Name 1": "https://path/to/rss.xml", 
    "Example News 2": "http://path/to/latest.rss"
  } 
}
"""


class SilentHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        if action.dest in ('height', 'width', 'locality'):
            return ''
        return super()._format_action(action)


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=SilentHelpFormatter
    )

    parser.add_argument(
        '--config', type=str, default='./newsterm/config.json',
        help='Path to the configuration file (default: ./newsterm/config.json)'
    )
    parser.add_argument(
        '--width', type=int, default=80,
        help='Width of the terminal (default: 80)'
    )
    parser.add_argument(
        '--height', type=int, default=24,
        help='Height of the terminal (default: 24)'
    )
    parser.add_argument(
        '--delay', type=int, default=120,
        help='Number of seconds to pause between each refresh (default: 120 seconds)'
    )
    parser.add_argument(
        '--locality', type=str, default='Europe/London',
        help="A timezone region in which to present the feed results (default: Europe/London)"
    )

    parser.add_argument(
        '--ignore-future', action='store_false',
        help="Ignore entries which are dated in the future"
    )

    parser.add_argument(
        '--extended-help', action='store_true',
        help="Show extended help for options --locality, --width, --height"
    )

    args = parser.parse_args()

    if args.extended_help:
        show_extended_help()
    else:
        sources = get_sources(filepath=args.config)
        local_timezone = timezone(args.locality)
        terminal = Terminal(sources, dimensions=(args.width, args.height), interval_secs=args.delay,
                            locality=local_timezone, ignore_future=args.ignore_future)
        terminal.run()


def show_extended_help():

    print('Extended Help:\n')
    print('--config: Path to the configuration file (default: ./newsterm/config.json)')
    print('  Specify the path to the configuration file used to load settings for the RSS dashboard.\n')
    print('--width: Width of the terminal (default: 80)')
    print('  Set the width of the terminal display area. Adjust as needed for your terminal window.\n')
    print('--height: Height of the terminal (default: 24)')
    print('  Set the height of the terminal display area. Adjust to fit your terminal window.\n')
    print('--delay: Number of seconds to pause between each refresh (default: 30 seconds)')
    print('  Define the interval in seconds between each refresh of the feed data.\n')
    print('--locality: A timezone region in which to present the feed results (default: Europe/London)')
    print('  Set the timezone region used for presenting the feed results. Specify the region as an integer.')


if __name__ == '__main__':
    main()
