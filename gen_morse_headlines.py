# Copyright (c) 2024 Mark Jenkins <mark@markjenkins.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from datetime import datetime, timedelta
from time import mktime
from random import shuffle
from sys import argv
from os.path import exists
from importlib import import_module

# the cduck_morse code doesn't come as an installable package
# my version with workableAsLibrary branch
# https://github.com/markjenkins/cduck_morse/tree/workableAsLibrary
# works by including an __init__.py and changing the import statements
#
# name the directory cduck_morse and make available the python path
# My version is also available in this project as a sub-module
from cduck_morse.play import FREQ, main as cduck_play_main
from cduck_morse.morseTable import forwardTable as MORSE_TABLE

# set to change tone frequency
#FREQ=FREQ

# python3-feedparser package in debian
from feedparser import parse as feedparser_parse

# I will be adding more feeds, this is just my minimal viable product
FEED_MODULE_NAMES=[
    'cp_via_cno', # CP articles published by CNO
]

# load_feed_module loads a python module by name
#
# why a fancy module architechure? Because different feeds will end up
# having different feed field, filtering and char substitution requirements
#
# this will be useful in a later version where I will have the option to ask
# a large language model service to write its own short summaries/headlines,
# and so there will be filtering requirements on the articles
#
# reason for that rabbit hole will be to allow re-publication, as LLM
# generated summaries should be publishable with the original source noted and
# disclosure of the LLM involvment. To republish an existing collection of
# original headlines could be seen as copyright infringement.
#
# for private use, using the publisher's headlines/summaries will always
# remain an option
def load_feed_module(module):
    try:
        return import_module(module)
    except ImportError: return None

# yes, nesting an if statement inside a for statement would have been
# an okay way to do this. What can I say, I like list comprehensions
FEED_MODS = [ mod for mod in [ load_feed_module(mod_name)
                               for mod_name in FEED_MODULE_NAMES ]
              if mod is not None ]

# CUTOFF_DAYS is how many days backwards to include
# so 1 is just stories from the last day
#
# I used 3 when developing this on 2024-01-28, but 1 should be fine after
# I add more feeds
CUTOFF_DAYS = 1

def get_headlines(feed_mod, now, now_str):
    cutoff = now - timedelta(days=CUTOFF_DAYS)

    feed_url_or_path = (
        feed_mod.URL
        if not (hasattr(feed_mod, 'DEBUG_FILE_OVERRIDE') and
                exists(feed_mod.DEBUG_FILE_OVERRIDE) )
        else feed_mod.DEBUG_FILE_OVERRIDE)
    parsed_feed = feedparser_parse(feed_url_or_path)
    return [ ( getattr(entry, feed_mod.ENTRY_ATTRIBUTE) + ' ' +
               feed_mod.NAME + ' ' +
               "%d-%.2d-%.2d" % entry.published_parsed[:3]
              )
             for entry in parsed_feed.entries
             # only do articles past a cutoff
             if (datetime.fromtimestamp(mktime(entry.published_parsed))
                 > cutoff )
            ]

# 12/5 is Canadian amateur radio test standard
# eventually there will be multiple output speeds
#
# training at a higher speed recommended to develop instant
# character recognition
DEFAULT_WPM = 12
DEFAULT_FS = 5

SHUFFLE = True # False may help when debugging
MAX_STORIES = 10

PREFIX_MSG_TEMPLATE = 'VVV VVV VVV daily RSS feeds for %s VVV'

def main():
    now = datetime.now()
    now_str = '%d-%.2d-%.2d' % (now.year, now.month, now.day)
    headlines = [
        headline
        for feed_mod in FEED_MODS
        for headline in get_headlines(feed_mod, now, now_str)
        ]

    headlines = headlines[:MAX_STORIES]

    if len(headlines)==0:
        headlines.append( 'no headlines today' )

    if SHUFFLE:
        shuffle(headlines) # less predictable when multiple agencies are in feed

    # join headline texts together
    #
    # prosign <BR> would be nice between stories as well at some point,
    # but multichar inputs are not yet supported.. perhaps there's a good
    # choice of single ASCII char we could use to add <BR> faster
    #
    # I plan to still keep the pace setting VVVs as well
    headlines_as_one_str = ' VVV '.join(headlines)

    prefix_msg = PREFIX_MSG_TEMPLATE % now_str

    transcript = prefix_msg + ' ' + headlines_as_one_str
    # filter out chars that are not in the morse table
    # should eventually log this so substitutes can be put in place
    transcript = ''.join( c
                          for c in transcript.upper()
                          if c in MORSE_TABLE or c==' ' )

    cduck_play_main(transcript, # message
                    FREQ, # freq
                    DEFAULT_WPM, # wpm
                    DEFAULT_FS, # fs
                    None, # prompt
                    argv[1]) # outFile output filename
    with open(argv[1] + '.txt', 'w') as f:
        f.write(transcript)

if __name__ == "__main__":
    main()
