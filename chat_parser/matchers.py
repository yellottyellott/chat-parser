from __future__ import unicode_literals

import logging
import re

from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import html

logger = logging.getLogger(__name__)


class Matcher(object):
    """
    Finds all matches of pattern.

    `pattern` must be defined in subclassses. Matches are case insensitive
    by default.

    `pattern` should be defined with 1 matching group to return as the
    matching token.
    """
    regex = None

    def __init__(self, pattern=None):
        if pattern:
            self.regex = re.compile(pattern)

    def matches(self, string):
        if not self.regex:
            raise NotImplementedError(".regex must be defined.")

        matches = self.get_matches(string)
        matches = self.clean_matches(matches)
        return matches

    def get_matches(self, string):
        matches = self.regex.finditer(string)
        matches = [m.group(1) for m in matches]
        return matches

    def clean_matches(self, matches):
        """Manipulate matches before returning."""
        return list(set(map(lambda s: s.lower(), matches)))


class MentionMatcher(Matcher):
    """
    Finds all @mentions in a string.
    """
    regex = re.compile('@(\w+)')


class EmoticonMatcher(Matcher):
    """
    Finds all (emoticons) in a string.
    """
    regex = re.compile('\(([a-zA-Z0-9]{1,15})\)')


class LinkMatcher(Matcher):
    """
    Finds all links in a string.

    These guys are smarter than me:
        https://mathiasbynens.be/demo/url-regex
        https://gist.github.com/dperini/729294#comment-1296121
    """
    regex = re.compile(
        '(?:\s|^)'
        '('
            '(?:(?:https?|s?ftp)://)?'  # scheme
            '(?:\S+(?::\S*)?@)?'  # auth
            '(?:'
                '(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'  # NOQA ipv4
                '|'
                '(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)'  # NOQA host
                '(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*'  # NOQA domain
                '(?:\.(?:[a-z\u00a1-\uffff]{2,}))'  # tld
            ')'
            '(?::\d{2,5})?'  # port
            '(?:/\S*)?'  # resource
        ')'
    )

    def clean_matches(self, matches):
        """Fetch the url titles."""
        data = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            for url in matches:
                future = executor.submit(fetch_title, url)
                data.append({
                    "url": url,
                    "title": future.result(),
                })

        return data


def fetch_title(url):
    """
    Fetches the title for a given url.

    If the url is not a web page or there is an error fetching the
    page, an empty string, '', is returned.
    """
    logger.debug("Fetching title for: {}".format(url))

    scheme = '(https?|ftps?)://'
    if not re.match(scheme, url):
        url = 'http://' + url

    if not url.startswith('http'):
        return ''

    try:
        page = requests.get(url, timeout=4)
    except requests.exceptions.RequestException:
        logger.info("Fetching url: {} timed out.".format(url))
        return ''

    try:
        # XXX: I assume this can throw a ParseError, but I can't find the
        # stupid documentation on it.
        # Supposedly:
        #   "It will not raise an exception on parser errors. You should
        #   use libxml2 version 2.6.21 or newer to take advantage of this
        #   feature."
        # But I find that hard to believe.
        tree = html.fromstring(page.text)
    except:
        logger.info("Error parsing page from: {}".format(url))
        return ''

    el = tree.find(".//title")
    if el is None:
        return ''

    return el.text
