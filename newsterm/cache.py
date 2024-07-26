class Cache:

    def __init__(self):
        self.cache = {}

    def add_list(self, candidates: list):
        """ Adds a list of candidate stories to the cache.

        :param candidates: A list of Story objects
        :return: None
        """
        for candidate in candidates:
            if (candidate.source, candidate.title) not in self.cache.keys():
                self.cache[(candidate.source, candidate.title)] = candidate

    def get_most_recent_entries(self, number_stories) -> list:
        """ Returns the most recent stories in the cache
        
        :param number_stories: The number of stories to return
        :return: List of Story objects
        """
        all_stories = [story for story in self.cache.values()]
        sorted_stories = sorted(all_stories, key=lambda story: story.datetime, reverse=True)
        return sorted_stories[:number_stories]
