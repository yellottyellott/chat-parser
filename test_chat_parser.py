# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        assert matches == []

    def test_mention(self):
        string = "With @jake the dog!"
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_multiple(self):
        string = "With @jake the dog! And @finn the human,"
        matches = self.matcher.matches(string)
        assert matches == ["jake", "finn"]

    def test_nonword_characters(self):
        string = "With @!c3k!ng the wizard!"
        matches = self.matcher.matches(string)
        assert matches == []

        string = "With @ic3_k!ng the wizard!"
        matches = self.matcher.matches(string)
        assert matches == ["ic3_k"]

    def test_same_nick_mentioned_multiple_times(self):
        """Verifies mentions are only returned once.

        If a nickname is mentioned multiple times, make sure it's
        only returned once.
        """
        string = "With @jake the dog! And @jake the dog,"
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_case_insensitivity(self):
        """Verify case insensitivity.

        If multiple mentions of the same nickname with different casing
        exist, make sure it's only returned once.
        """
        string = "With @Jake the dog! And @JAKE the dog,"
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_all_mention(self):
        """@all is a builtin mention."""
        string = "@all The fun will never end!"
        matches = self.matcher.matches(string)
        assert matches == ["all"]

    def test_here_mention(self):
        """@here is a built in mention."""
        string = "@here It's Adventure Time!"
        matches = self.matcher.matches(string)
        assert matches == ["here"]


class TestEmoticonMatcher(object):
    """
    Verifies EmoticonMatcher correctly finds all emoticons in a string.
    """
    def setup_method(self, method):
        self.matcher = matchers.EmoticonMatcher()

    def test_no_emoticons(self):
        string = "Adventure time! Come on, grab your friends."""
        matches = self.matcher.matches(string)
        assert matches == []

    def test_emoticon(self):
        string = "(jake) the dog!"
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_multiple(self):
        string = "(jake) the dog! and (finn) the human!"
        matches = self.matcher.matches(string)
        assert matches == ["jake", "finn"]

    def test_same_emoticon_sent_multiple_times(self):
        """Verify emoticons are only returned once.

        If an emoticon is mentioned mutliple times, make sure it's
        only returend once.
        """
        string = "(jake)(jake)(jake). (jake)(jake)(jake). (jake) your booty."
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_case_insensitivity(self):
        """Verify case insensitivity.

        If multiple instances of the same emoticon with different casing
        exist, make sure it's only returned once.
        """
        string = "(jake) the dog. (Jake) The Dog. (JAKE) THE DOGGGG!!!"
        matches = self.matcher.matches(string)
        assert matches == ["jake"]

    def test_numbers(self):
        string = "Science. Is. (mathematical123)!"
        matches = self.matcher.matches(string)
        assert matches == ["mathematical123"]

    def test_underscores(self):
        string = "(jake_the_dog) is not a valid emoticon."
        matches = self.matcher.matches(string)
        assert matches == []

    def test_whitespace(self):
        string = "(jake the dog) is not a valid emoticon."
        matches = self.matcher.matches(string)
        assert matches == []

    def test_character_length(self):
        """Verify emoticons are no longer than 15 characters.
        """
        string = "()"  # 0
        matches = self.matcher.matches(string)
        assert matches == []

        string = "(mathematical123)"  # 15
        matches = self.matcher.matches(string)
        assert matches == ["mathematical123"]

        string = "(mathematical1234)"  # 16
        matches = self.matcher.matches(string)
        assert matches == []


class TestLinkMatcher(object):
    """
    Verifies EmoticonMatcher correctly finds all emoticons in a string.
    """
    def setup_method(self, method):
        self.matcher = matchers.LinkMatcher()

    def test_no_links(self):
        string = "It came from the night-o-sphere. bum .bum .bum."
        matches = self.matcher.get_matches(string)
        assert matches == []

    def test_link(self):
        sweet_vid = "https://www.youtube.com/watch?v=aZdtZIuVzmE"
        string = "Finn, check it: {}".format(sweet_vid)
        matches = self.matcher.get_matches(string)
        assert matches == [sweet_vid]

    def test_multiple(self):
        vid1 = "https://www.youtube.com/watch?v=IZHnWvMaoKM"
        vid2 = "https://www.youtube.com/watch?v=dGGk8y_s9uQ"
        string = "Watch this: {} and this: {}".format(vid1, vid2)
        matches = self.matcher.get_matches(string)
        assert matches == [vid1, vid2]

    def test_multiline_matching(self):
        vid = "https://www.youtube.com/watch?v=dGGk8y_s9uQ"
        string = """
            Makin' pancakes!
            Makin' bacon pancakes!
            Bacon pancaaakkkeeessss: {}
            """.format(vid)
        matches = self.matcher.get_matches(string)
        assert matches == [vid]

    def test_no_surrounding_whitespace(self):
        """We're only matching links surrounded by whitespace."""
        string = "Don't visit _night-o-sphere.com_. It's too scary."
        matches = self.matcher.get_matches(string)
        assert matches == []

    def test_valid_links(self):
        """Finding links is hard."""
        valid_urls = [
            # u'http://💩.la/', :(((
            "http://foo.com/blah_blah",
            "http://foo.com/blah_blah/",
            "http://foo.com/blah_blah_(wikipedia)",
            "http://foo.com/blah_blah_(wikipedia)_(again)",
            "http://www.example.com/wpstyle/?p=364",
            "https://www.example.com/foo/?bar=baz&inga=42&quux",
            "http://✪df.ws/123",
            "http://userid:password@example.com:8080",
            "http://userid:password@example.com:8080/",
            "http://userid@example.com",
            "http://userid@example.com/",
            "http://userid@example.com:8080",
            "http://userid@example.com:8080/",
            "http://userid:password@example.com",
            "http://userid:password@example.com/",
            "http://142.42.1.1/",
            "http://142.42.1.1:8080/",
            "http://➡.ws/䨹",
            "http://⌘.ws",
            "http://⌘.ws/",
            "http://foo.com/blah_(wikipedia)#cite-1",
            "http://foo.com/blah_(wikipedia)_blah#cite-1",
            "http://foo.com/unicode_(✪)_in_parens",
            "http://foo.com/(something)?after=parens",
            "http://☺.damowmow.com/",
            "http://code.google.com/events/#&product=browser",
            "http://j.mp",
            "ftp://foo.bar/baz",
            "http://foo.bar/?q=Test%20URL-encoded%20stuff",
            "http://مثال.إختبار",
            "http://例子.测试",
            "http://उदाहरण.परीक्षा",
            "http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
            "http://1337.net",
            "http://a.b-c.de",
            "http://223.255.255.254",

            "www.google.com/search?q=adventure%20time",
            "adventuretime.com",
            "adventuretime.com/finn",
            "jake@adventuretime.com",
            "0.0.0.0:8000/login/",
            "finn:thehuman@10.0.0.1",
        ]
        for url in valid_urls:
            matches = self.matcher.get_matches(url)
            assert matches == [url]

    def test_invalid_links(self):
        invalid_urls = [
            "http://",
            "http://.",
            "http://..",
            "http://../",
            "http://?",
            "http://??",
            "http://??/",
            "http://#",
            "http://##",
            "http://##/",
            "//",
            "//a",
            "///a",
            "///",
            "http:///a",
            "rdar://1234",
            "h://test",
            ":// should fail",
            "http://-error-.invalid/",
            "http://a.b--c.de/",
            "http://-a.b.co",
            "http://a.b-.co",
            "http://123.123.123",
            "http://3628126748",
            "http://.www.foo.bar/",
            "http://.www.foo.bar./",
        ]
        for url in invalid_urls:
            matches = self.matcher.get_matches(url)
            assert matches == []
