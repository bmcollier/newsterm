import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import feedparser

from newsterm.feeds import get_latest_updates
from newsterm.story import Story


class TestFeeds(unittest.TestCase):

    @patch('feedparser.parse')
    def test_get_latest_updates(self, MockFeedparserParse):
        mock_feedparser_result = MagicMock()
        mock_feedparser_result.entries = [
            MagicMock(
                published='Fri, 26 Jul 2024 12:34:56 GMT',
                title='Test Title 1',
                summary='Test Summary 1'
            ),
            MagicMock(
                published='Sat, 27 Jul 2024 13:45:00 GMT',
                title='Test Title 2',
                summary='Test Summary 2'
            )
        ]
        MockFeedparserParse.return_value = mock_feedparser_result

        sources = {
            "sources": {
                "source1": "http://example.com/rss1",
                "source2": "http://example.com/rss2"
            }
        }

        result = get_latest_updates(sources)

        expected_tz = timezone(timedelta(hours=1))
        expected_dt1 = datetime(2024, 7, 26, 13, 34, 56, tzinfo=expected_tz)
        expected_dt2 = datetime(2024, 7, 27, 14, 45, 00, tzinfo=expected_tz)

        expected_result = [
            # Source 1 Stories
            Story(source='source1', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source1', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),

            # Source 2 Stories (same entries as source 1 but different source)
            Story(source='source2', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source2', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),
        ]

        self.assertEqual(result, expected_result)

    @patch('feedparser.parse')
    def test_get_latest_unexpected_dt_format(self, MockFeedparserParse):
        mock_feedparser_result = MagicMock()
        mock_feedparser_result.entries = [
            MagicMock(
                published='Tue, 30 Jul 2024 01:07:50 -0400',
                title='Test Title 1',
                summary='Test Summary 1'
            ),
            MagicMock(
                published='Tue, 30 Jul 2024 01:09:20 -0400',
                title='Test Title 2',
                summary='Test Summary 2'
            )
        ]
        MockFeedparserParse.return_value = mock_feedparser_result

        sources = {
            "sources": {
                "source1": "http://example.com/rss1",
                "source2": "http://example.com/rss2"
            }
        }

        result = get_latest_updates(sources)

        expected_tz = timezone(timedelta(hours=1))
        expected_dt1 = datetime(2024, 7, 30, 6, 7, 50, tzinfo=expected_tz)
        expected_dt2 = datetime(2024, 7, 30, 6, 9, 20, tzinfo=expected_tz)

        expected_result = [
            # Source 1 Stories
            Story(source='source1', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source1', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),

            # Source 2 Stories (same entries as source 1 but different source)
            Story(source='source2', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source2', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),
        ]

        self.assertEqual(result, expected_result)

    @patch('feedparser.parse')
    def test_get_latest_unexpected_dt_format_no_dst(self, MockFeedparserParse):
        mock_feedparser_result = MagicMock()
        mock_feedparser_result.entries = [
            MagicMock(
                published='Tue, 30 Jan 2024 01:07:50 -0400',
                title='Test Title 1',
                summary='Test Summary 1'
            ),
            MagicMock(
                published='Tue, 30 Jan 2024 01:09:20 -0400',
                title='Test Title 2',
                summary='Test Summary 2'
            )
        ]
        MockFeedparserParse.return_value = mock_feedparser_result

        sources = {
            "sources": {
                "source1": "http://example.com/rss1",
                "source2": "http://example.com/rss2"
            }
        }

        result = get_latest_updates(sources)

        expected_tz = timezone(timedelta(hours=0))
        expected_dt1 = datetime(2024, 1, 30, 5, 7, 50, tzinfo=expected_tz)
        expected_dt2 = datetime(2024, 1, 30, 5, 9, 20, tzinfo=expected_tz)

        expected_result = [
            # Source 1 Stories
            Story(source='source1', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source1', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),

            # Source 2 Stories (same entries as source 1 but different source)
            Story(source='source2', title='Test Title 1', summary='Test Summary 1', datetime=expected_dt1),
            Story(source='source2', title='Test Title 2', summary='Test Summary 2', datetime=expected_dt2),
        ]

        self.assertEqual(result, expected_result)