from chat_parser import matchers


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
