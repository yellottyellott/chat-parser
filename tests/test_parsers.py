import mock

from chat_parser.parsers import Parser, parse


class TestParser(object):
    def setup_method(self, method):
        self.parser = Parser()

    def test_parse(self):
        string = "@jake, jake.com is up. (thumbsup)"

        def mock_get(url, timeout):
            return mock.Mock(text="<title>Jake</title>")

        with mock.patch('requests.get', mock_get):
            data = self.parser.parse(string)

        expected_data = {
            'mentions': ['jake'],
            'emoticons': ['thumbsup'],
            'links': [{'url': 'jake.com', 'title': 'Jake'}]
        }
        assert data == expected_data

    def test_serialize(self):
        data = {
            'mentions': ['jake'],
            'emoticons': ['thumbsup'],
            'links': [{'url': 'jake.com', 'title': 'Jake'}]
        }
        self.parser.serialize(data)


class TestParseFunction(object):
    def test_parse(self):
        string = "@jake, jake.com is up. (thumbsup)"

        def mock_get(url, timeout):
            return mock.Mock(text="<title>Jake</title>")

        with mock.patch('requests.get', mock_get):
            parse(string)
