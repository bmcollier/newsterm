from newsterm.core import run

if __name__ == '__main__':
    sources = {
        "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
        "CNN": "http://rss.cnn.com/rss/cnn_latest.rss"
        #"Reuters": "https://www.reutersagency.com/feed/?best-types=reuters-news-first&post_type=best"
    }
    options = {
        "REFRESH_INTERVAL_SECS": 10,
        "SHOW_STORIES_NUM": 10
    }
    num_sources = len(sources)
    if options.get("REFRESH_INTERVAL_SECS") is None:
        raise ValueError("No refresh interval supplied")
    if num_sources == 0:
        raise ValueError("No sources supplied")
    run(list(sources.items()), options)
