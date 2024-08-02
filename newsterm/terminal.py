from time import sleep
from pytz import timezone

from newsterm.display import Display
from newsterm.cache import Cache
from newsterm.feeds import get_latest_updates


class Terminal:

    def __init__(self, sources: dict, dimensions: tuple, interval_secs: int, locality: timezone, include_future: bool,
                 num_stories: int, lines_per_story: int, max_pages: int):
        self.sources = sources
        self.dimensions = dimensions
        self.interval_secs = interval_secs
        self.locality = locality
        self.include_future = include_future
        self.num_stories = num_stories
        self.lines_per_story = lines_per_story
        self.max_pages = max_pages

    def run(self, run_once: bool = False):
        """ Primary run loop - call sources and update terminal
        :return:
        """

        # Initialise system
        display = Display(self.dimensions)
        cache = Cache()
        interval_counter = 0

        print("Loading initial sources...")

        # Initialise Cache
        latest_updates = get_latest_updates(self.sources, self.locality, self.include_future)
        cache.add_list(latest_updates)

        # Run until quit
        while True:
            if display.quit_requested():
                break
            sleep(1)
            if interval_counter % self.interval_secs == 0:
                latest_updates = get_latest_updates(self.sources, self.locality, self.include_future)
                cache.add_list(latest_updates)
                display.update(cache.get_most_recent_entries(self.num_stories))
                interval_counter = 0
            interval_counter += 1
            if run_once:
                break

        # Quit cleanly
        display.clean_quit()
        print("\n\nThanks for using Newsterm!")

