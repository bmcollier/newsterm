from unittest import TestCase
from datetime import datetime

from newsterm.cache import Cache
from newsterm.story import Story


class TestCache(TestCase):

    def test_add(self):
        """ When I add a story to the cache, it is stored. """
        cache = Cache()
        story_source = "Example Source"
        story_title = "Example Title"
        story_summary = "Example Summary"
        story_dt = datetime.now()
        new_story = Story(story_source, story_title, story_summary, story_dt)
        story_list = [new_story]
        cache.add_list(story_list)
        self.assertEqual(cache.cache.get((story_source, story_title)).summary, story_summary)

    def test_add_duplicate(self):
        """ When I add a duplicate to the cache, it is not stored, and the original datetime remains in place. """
        cache = Cache()
        story_source = "Example Source"
        story_title = "Example Title"
        story_summary = "Example Summary"
        story_dt = datetime(2024, 7, 25, 12, 30, 45)
        new_story = Story(story_source, story_title, story_summary, story_dt)
        story_list = [new_story]
        cache.add_list(story_list)
        cache.add_list(story_list)
        self.assertEqual(len(cache.cache), 1)

    def test_most_recent_entries(self):
        """ When I add a selection of stories, they are returned most-recent first. """
        cache = Cache()
        story_source = "Example Source"
        story_title_1 = "Example Title 1"
        story_title_2 = "Example Title 2"
        story_title_3 = "Example Title 3"
        story_summary = "Example Summary"
        story_dt_1 = datetime(2024, 7, 25, 12, 30, 45)
        story_dt_2 = datetime(2024, 7, 25, 13, 30, 45)
        story_dt_3 = datetime(2024, 7, 26, 11, 30, 45)
        new_story_1 = Story(story_source, story_title_1, story_summary, story_dt_1)
        new_story_2 = Story(story_source, story_title_2, story_summary, story_dt_2)
        new_story_3 = Story(story_source, story_title_3, story_summary, story_dt_3)
        story_list = [new_story_3, new_story_1, new_story_2]
        cache.add_list(story_list)
        cached_stories = cache.get_most_recent_entries(3)
        self.assertEqual(len(cached_stories), 3)
        self.assertEqual(cached_stories[0].datetime, datetime(2024, 7, 26, 11, 30, 45))
        self.assertEqual(cached_stories[1].datetime, datetime(2024, 7, 25, 13, 30, 45))
        self.assertEqual(cached_stories[2].datetime, datetime(2024, 7, 25, 12, 30, 45))
