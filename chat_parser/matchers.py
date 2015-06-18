import re


class MentionMatcher(object):
    """
    Finds all @mentions in a string.

    If the same nickname is mentioned more than once, the nickname is
    only returned once.

    @mentions are case insensitive.
    """
    pattern = r'@(\w+)'

    def matches(self, string):
        """Returns all @mention matches in `string`, stripping off the
        leading @ character.
        """
        matches = re.finditer(self.pattern, string)
        tokens = set(m.group(1).lower() for m in matches)
        return tokens
