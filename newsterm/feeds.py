import re
from datetime import datetime
from dateutil import parser
from pytz import timezone

import feedparser
from unidecode import unidecode

from newsterm.story import Story


def get_latest_updates(sources: dict, locality: timezone, include_future: bool) -> list:
    """ Calls each source and populates a list with Story objects from the sources

    :param sources: A list of RSS feeds to check
    :param locality: A local timezone
    :param ignore_future: Ignore feed items dated in the future
    :return: A list of Story objects returned from the RSS feeds
    """
    latest_updates = []
    for source_name, source_url in sources["sources"].items():
        latest_update = feedparser.parse(source_url)
        for entry in latest_update.entries:
            try:
                published_dt = parser.parse(entry.published)
                localised_datetime = published_dt.astimezone(locality)
                if (not include_future) and (localised_datetime > datetime.now(locality)):
                    continue
                new_story = Story(source=source_name,
                                  title=unidecode(entry.title),
                                  summary=(unidecode(remove_html_markup(entry.summary))),
                                  datetime=localised_datetime,
                                  retrieved=datetime.now(locality))
            except AttributeError:
                published_dt = datetime.now(locality)
                new_story = Story(source=source_name,
                                  title="ERROR. This source is missing a required attribute. Check the RSS.",
                                  summary="This can happen if a publication omits a 'published' datetime.",
                                  datetime=published_dt,
                                  retrieved=datetime.now(locality))

            latest_updates.append(new_story)
    return latest_updates


def remove_html_markup(text):
    # Replace specific tags with a space
    text = re.sub(r'</p>\s*<p>', ' ', text)
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'<li\s*/?>', ' ', text)

    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove any extra spaces that may result from substitutions
    text = re.sub(r'\s+', ' ', text).strip()

    return text