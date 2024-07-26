import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Newsterm - Run an RSS dashboard in a terminal",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = DESCRIPTION

    parser.add_argument('--config', type=str, default='./newsterm/config.json',
                        help='Path to the configuration file (default: ./newsterm/config.json)')
    parser.add_argument('--width', type=int, default=80, help='Width of the terminal (default: 80)')
    parser.add_argument('--height', type=int, default=24, help='Height of the terminal (default: 24)')
    parser.add_argument('--delay', type=int, default=30,
                        help='Number of seconds to pause between each refresh (default: 30 seconds)')

    args = parser.parse_args()

    sources = get_sources(filepath=args.config)
    terminal = Terminal(sources, dimensions=(args.width, args.height), interval_secs=args.delay)
    terminal.run()
