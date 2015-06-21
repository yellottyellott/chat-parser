import pytest

from chat_parser import matchers


class TestMatcher(object):
    """
    Tests the base Matcher class.
    """
    def test_pattern_not_defined(self):
        matcher = matchers.Matcher()
        string = "Adventure time! Come on, grab your friends."""

        with pytest.raises(NotImplementedError):
            matcher.matches(string)


class TestMentionMatcher(object):
    """
    Verifies MentionMatcher correctly finds all mentions in a string.
    """
    def setup_method(self, method):
        self.matcher = matchers.MentionMatcher()

    def test_no_mentions(self):
        string = "Adventure time! Come on, grab your friends."""
        matches = self.matcher.matches(string)
        assert matches == set()

    def test_mention(self):
        string = "With @jake the dog!"
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_multiple(self):
        string = "With @jake the dog! And @finn the human,"
        matches = self.matcher.matches(string)
        assert matches == set(["jake", "finn"])

    def test_nonword_characters(self):
        string = "With @!c3k!ng the wizard!"
        matches = self.matcher.matches(string)
        assert matches == set()

        string = "With @ic3_k!ng the wizard!"
        matches = self.matcher.matches(string)
        assert matches == set(["ic3_k"])

    def test_same_nick_mentioned_multiple_times(self):
        """Verifies mentions are only returned once.

        If a nickname is mentioned multiple times, make sure it's
        only returned once.
        """
        string = "With @jake the dog! And @jake the dog,"
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_case_insensitivity(self):
        """Verify case insensitivity.

        If multiple mentions of the same nickname with different casing
        exist, make sure it's only returned once.
        """
        string = "With @Jake the dog! And @JAKE the dog,"
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_all_mention(self):
        """@all is a builtin mention."""
        string = "@all The fun will never end!"
        matches = self.matcher.matches(string)
        assert matches == set(["all"])

    def test_here_mention(self):
        """@here is a built in mention."""
        string = "@here It's Adventure Time!"
        matches = self.matcher.matches(string)
        assert matches == set(["here"])


class TestEmoticonMatcher(object):
    """
    Verifies EmoticonMatcher correctly finds all emoticons in a string.
    """
    def setup_method(self, method):
        self.matcher = matchers.EmoticonMatcher()

    def test_no_emoticons(self):
        string = "Adventure time! Come on, grab your friends."""
        matches = self.matcher.matches(string)
        assert matches == set()

    def test_emoticon(self):
        string = "(jake) the dog!"
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_multiple(self):
        string = "(jake) the dog! and (finn) the human!"
        matches = self.matcher.matches(string)
        assert matches == set(["jake", "finn"])

    def test_same_emoticon_sent_multiple_times(self):
        """Verify emoticons are only returned once.

        If an emoticon is mentioned mutliple times, make sure it's
        only returend once.
        """
        string = "(jake)(jake)(jake). (jake)(jake)(jake). (jake) your booty."
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_case_insensitivity(self):
        """Verify case insensitivity.

        If multiple instances of the same emoticon with different casing
        exist, make sure it's only returned once.
        """
        string = "(jake) the dog. (Jake) The Dog. (JAKE) THE DOGGGG!!!"
        matches = self.matcher.matches(string)
        assert matches == set(["jake"])

    def test_numbers(self):
        string = "Science. Is. (mathematical123)!"
        matches = self.matcher.matches(string)
        assert matches == set(["mathematical123"])

    def test_underscores(self):
        string = "(jake_the_dog) is not a valid emoticon."
        matches = self.matcher.matches(string)
        assert matches == set()

    def test_whitespace(self):
        string = "(jake the dog) is not a valid emoticon."
        matches = self.matcher.matches(string)
        assert matches == set()

    def test_character_length(self):
        """Verify emoticons are no longer than 15 characters.
        """
        string = "()"  # 0
        matches = self.matcher.matches(string)
        assert matches == set()

        string = "(mathematical123)"  # 15
        matches = self.matcher.matches(string)
        assert matches == set(["mathematical123"])

        string = "(mathematical1234)"  # 16
        matches = self.matcher.matches(string)
        assert matches == set()
