Newsterm: A VT-100 compatible RSS dashboard
===========================================

usage: main.py [-h] [--config CONFIG] [--width WIDTH] [--height HEIGHT]
               [--delay DELAY]

Newsterm runs in a terminal window, and works well on a VT100 terminal. The
size of the window can be configured, as can the delay between RSS calls.

The config file takes the following JSON format:

{
  "sources": {
    "Source Name 1": "https://path/to/rss.xml", 
    "Example News 2": "http://path/to/latest.rss"
  } 
}

options:

  -h, --help       show this help message and exit

  --config CONFIG  Path to the configuration file (default: ./config.json)

  --width WIDTH    Width of the terminal (default: 80)

  --height HEIGHT  Height of the terminal (default: 24)

  --delay DELAY    Number of seconds to pause between each refresh (default:
                   30 seconds)

Please be aware that I'm still implementing the height and width control.
