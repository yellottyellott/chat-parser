from __future__ import unicode_literals

import mock
import json

from chat_parser.handlers import Handler, parse


class TestHandler(object):
    def setup_method(self, method):
        self.handler = Handler()

    def test_parse(self):
        string = "@jake, jake.com is up. (thumbsup)"

        def mock_get(url, timeout):
            return mock.Mock(text="<title>Jake</title>")

        with mock.patch('requests.get', mock_get):
            data = self.handler.parse(string)

        expected_data = {
            'mentions': ['jake'],
            'emoticons': ['thumbsup'],
            'links': [{'url': 'jake.com', 'title': 'Jake'}]
        }
        assert data == expected_data

    def test_parse_with_missing_keys(self):
        """Verify emtpy keys are missing."""
        string = "@jake is makin bacon pancakes."
        expected_data = {'mentions': ['jake']}
        data = self.handler.parse(string)
        assert data == expected_data

    def test_serialize(self):
        data = {
            'mentions': ['jake'],
            'emoticons': ['thumbsup'],
            'links': [{'url': 'jake.com', 'title': 'Jake'}]
        }
        # JSON encoding has non deterministic ordering.
        # Verify it serializes.
        self.handler.serialize(data)


class TestParseFunction(object):
    def test_parse(self):
        string = "@jake, jake.com is up. (thumbsup)"

        def mock_get(url, timeout):
            return mock.Mock(text="<title>Jake</title>")

        with mock.patch('requests.get', mock_get):
            string = parse(string)

        data = json.loads(string)

        assert data['mentions'] == ['jake']
        assert data['emoticons'] == ['thumbsup']
        assert data['links'] == [{'url': 'jake.com', 'title': 'Jake'}]
