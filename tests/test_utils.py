from unittest import TestCase

from json.decoder import JSONDecodeError

from newsterm.utils import get_sources

class TestUtils(TestCase):

    def test_good_file(self):
        source_file = get_sources("fixtures/good_file.json")
        self.assertEqual(source_file.get("sources").get("Example 1"),"http://google.com/news/rss.xml")
        self.assertEqual(source_file.get("sources").get("Example 2"), "https://aws.com/rss/cnn_latest.rss")

    def test_nonsense_file(self):
        with self.assertRaises(JSONDecodeError):
            sources = get_sources("fixtures/bad_file_1.json")

    def test_file_with_no_sources_section(self):
        with self.assertRaises(ValueError):
            sources = get_sources("fixtures/bad_file_2.json")

    def test_malformed_file(self):
        with self.assertRaises(ValueError):
            sources = get_sources("fixtures/bad_file_3.json")

    def test_malformed_key_file(self):
        with self.assertRaises(JSONDecodeError):
            sources = get_sources("fixtures/bad_file_4.json")

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            sources = get_sources("fixtures/not_there.json")


