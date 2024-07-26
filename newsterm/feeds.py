from datetime import datetime
from datetime import timedelta

import feedparser

from newsterm.story import Story


def get_latest_updates(sources: dict) -> list:
    """ Calls each source and populates a list with Story objects from the sources

    :param sources: A list of RSS feeds to check
    :return: A list of Story objects returned from the RSS feeds
    """
    latest_updates = []
    for source_name, source_url in sources["sources"].items():
        latest_update = feedparser.parse(source_url)
        for entry in latest_update.entries:

            published_dt = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            published_dt_local = published_dt + timedelta(hours=1)

            new_story = Story(source=source_name,
                              title=entry.title,
                              summary=entry.summary,
                              datetime=published_dt_local)

            latest_updates.append(new_story)
    return latest_updates
