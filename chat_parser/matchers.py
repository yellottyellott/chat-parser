from __future__ import unicode_literals

import re


class Matcher(object):
    """
    Finds all matches of pattern.

    `pattern` must be defined in subclassses. Matches are case insensitive
    by default.

    `pattern` should be defined with 1 matching group to return as the
    matching token.
    """
    pattern = None

    def __init__(self, pattern=None):
        if pattern:
            self.pattern = pattern

    def matches(self, string):
        if not self.pattern:
            raise NotImplementedError(".pattern must be defined.")

        matches = re.finditer(self.pattern, string)
        matches = set(m.group(1) for m in matches)
        matches = self.clean_matches(matches)

        return matches

    def clean_matches(self, matches):
        return set(map(lambda s: s.lower(), matches))


class MentionMatcher(Matcher):
    """
    Finds all @mentions in a string.
    """
    pattern = '@(\w+)'


class EmoticonMatcher(Matcher):
    """
    Finds all (emoticons) in a string.
    """
    pattern = '\(([a-zA-Z0-9]{1,15})\)'


class LinkMatcher(Matcher):
    """
    Finds all links in a string.

    These guys are smarter than me:
        https://mathiasbynens.be/demo/url-regex
        https://gist.github.com/dperini/729294#comment-1296121
    """
    pattern = (
        '(?:\s|^)'
        '('
            '(?:(?:https?|ftps?)://)?'  # scheme
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
        return matches
