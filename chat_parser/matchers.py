import re


class Matcher(object):
    """
    Finds all matches of pattern.

    `pattern` must be defined in subclassses. Matches are case insensitive.
    """
    pattern = None

    def __init__(self, pattern=None):
        if pattern:
            self.pattern = pattern

    def matches(self, string):
        if not self.pattern:
            raise NotImplementedError(".pattern must be defined.")

        matches = re.finditer(self.pattern, string)
        tokens = set(m.group(1).lower() for m in matches)
        return tokens


class MentionMatcher(Matcher):
    """
    Finds all @mentions in a string.
    """
    pattern = r'@(\w+)'


class EmoticonMatcher(Matcher):
    """
    Finds all (emoticons) in a string.
    """
    pattern = r'\(([a-zA-Z0-9]{1,15})\)'
