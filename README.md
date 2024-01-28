Create a daily morse code listening exercise ripped from the headlines.

Uses RSS feeds of media organizations.

Pull requests adding extremist organizations are not welcome. Fork.

Relies on https://github.com/cduck/morse/ to generate the morse code tones

My forked version
https://github.com/markjenkins/cduck_morse/tree/workableAsLibrary
is required to use as an importable library.

My forked version of cduck_morse is available in this project as
a git sub-module.
git clone --recurse-submodules https://github.com/markjenkins/morseheadlines
Will get you my application and the sub-module.

To use, run
python3 gen_morse_headlines.py today.wav
which will also generate a transcript today.wav.txt

When developing/debugging, it is polite to not hit the RSS feed servers over
and over. Download a cached version of the RSS files you're working with and
set the DEBUG_FILE_OVERRIDE attribute in the feed module.


Available feeds:
 * Canadian Press (CP) articles posted on CNO (Canada's National Observer)

More to come... only 1 included to make first commit a minimal viable product.