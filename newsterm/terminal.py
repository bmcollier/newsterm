from time import sleep

from newsterm.display import Display
from newsterm.cache import Cache
from newsterm.feeds import get_latest_updates

DEFAULT_DIMENSIONS = (80, 24)


class Terminal:

    def __init__(self, sources: dict, dimensions: tuple = DEFAULT_DIMENSIONS, interval_secs: int = 60,
                 config: str = './config.json'):
        self.sources = sources
        self.dimensions = dimensions
        self.interval_secs = interval_secs
        self.config = config

    def run(self):
        """ Primary run loop - call sources and update terminal
        :return:
        """

        # Initialise system
        display = Display(self.dimensions)
        cache = Cache()
        interval_counter = 0

        print("Loading initial sources...")

        # Initialise Cache
        latest_updates = get_latest_updates(self.sources)
        cache.add_list(latest_updates)

        # Run until quit
        while True:
            display.update(cache.get_most_recent_entries(10))
            if display.quit_requested():
                break
            sleep(1)
            if interval_counter == self.interval_secs:
                latest_updates = get_latest_updates(self.sources)
                cache.add_list(latest_updates)
                interval_counter = 0
            interval_counter += 1

        # Quit cleanly
        display.clean_quit()
        print("\n\nThanks for using Newsterm!")

