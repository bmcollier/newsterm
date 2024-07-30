from dateutil import parser
from pytz import timezone

import feedparser

from newsterm.story import Story


def get_latest_updates(sources: dict, locality: timezone) -> list:
    """ Calls each source and populates a list with Story objects from the sources

    :param sources: A list of RSS feeds to check
    :param locality: A local timezone
    :return: A list of Story objects returned from the RSS feeds
    """
    latest_updates = []
    for source_name, source_url in sources["sources"].items():
        latest_update = feedparser.parse(source_url)
        for entry in latest_update.entries:

            published_dt = parser.parse(entry.published)
            localised_datetime = published_dt.astimezone(locality)

            new_story = Story(source=source_name,
                              title=entry.title,
                              summary=entry.summary,
                              datetime=localised_datetime)

            latest_updates.append(new_story)
    return latest_updates
