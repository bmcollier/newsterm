from time import sleep
from collections import OrderedDict
from datetime import datetime

import feedparser
from feedparser import FeedParserDict

from newsterm.display import Display


def run(sources: list, options: dict):
    running = True
    call_interval = options.get("REFRESH_INTERVAL_SECS") / len(sources)
    sources_index = 0
    recent_content = [None] * len(sources)
    display = Display()
    last_published = None
    while running:
        latest_update = feedparser.parse(sources[sources_index][1])
        latest_update = enrich_with_source(latest_update, sources[sources_index][0])
        if recent_content[sources_index] != latest_update.entries:
            recent_content[sources_index] = latest_update
            top_stories = sort_all_content(recent_content, options.get("SHOW_STORIES_NUM"))
            display_top_stories(top_stories, display)
        sources_index += 1
        if sources_index == len(sources):
            sources_index = 0
        sleep(call_interval)


def enrich_with_source(latest_update, source:str):
    latest_update_enriched = latest_update
    for entry in latest_update_enriched.entries:
        entry["source"] = source
    return latest_update_enriched


def sort_all_content(recent_content: list, num_stories: int) -> OrderedDict:
    all_entries = []
    ordered_entries = OrderedDict()
    for content in recent_content:
        if content:
            all_entries.extend(content.entries)
    for index in range(0, num_stories):
        ordered_entries[index] = get_and_remove_most_recent_entry(all_entries)
    return ordered_entries


def get_and_remove_most_recent_entry(all_entries: list) -> FeedParserDict:
    index = 0
    most_recent_index = 0
    most_recent_datetime = None
    for entry in all_entries:
        published_dt = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        if published_dt:
            if (most_recent_datetime is None) or (published_dt > most_recent_datetime):
                most_recent_datetime = published_dt
                most_recent_index = index
        index += 1
    return all_entries.pop(most_recent_index)


def display_top_stories(stories: OrderedDict, display: Display):
    display.update(stories)
    # print("---------")
    # for index, content in stories.items():
    #     print(content.source + " " + content.published[17:22] + " " + content.get("title"))
    #     print(content.get("summary"))