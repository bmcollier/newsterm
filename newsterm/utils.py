import json

DEFAULT_FILEPATH = './newsterm/config.json'


def get_sources(filepath: str = DEFAULT_FILEPATH) -> dict:
    """ Load a list of URLs giving sources for RSS feeds

    :param filepath: Path to a JSON file containing URLs to RSS feeds
    :return: Dictionary of URLs to RSS feeds
    """
    with open(filepath, 'r') as f:
        source_file = json.load(f)
        if not source_file.get("sources"):
            raise ValueError("No source section found - please refer to --help for source file format")
        sources = source_file.get("sources")
        for key, value in sources.items():
            if not isinstance(value, str):
                raise ValueError("Source value must be a string - please refer to --help for source file format")
        return source_file
