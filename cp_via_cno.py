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

# This feed is Canadian Press (CP) articles posted on CNO
# (Canada's National Observer)

# CP does not publish public RSS feeds.

# if I ever find another publication with a CP feed or a feed containing
# CP stuff, I should look at deduplication


NAME = 'CP via CNO'
URL = 'https://www.nationalobserver.com/user/13/rss'

TITLE_ATTRIBUTE = 'title'
SUMMARY_ATTRIBUTE = 'summary'

ENTRY_ATTRIBUTES = [TITLE_ATTRIBUTE, SUMMARY_ATTRIBUTE]


# for development/debugging, downloading the file with curl/wget etc and
# enabling this is recommended to avoid hitting the server over and over
#DEBUG_FILE_OVERRIDE = 'CP_via_CNO_2024-01-28.rss'
