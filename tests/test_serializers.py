from chat_parser.serializers import JSONSerializer


class TestJSONSerializer(object):
    def test_serializer(self):
        data = {
            'mentions': ['jake', 'finny', 'ladyrainicorn'],
            'emoticons': ['breadcrubs', 'thumbsup'],
            'link': [
                {'url': 'lumpyspace.com', 'title': "What the Lump!"},
            ]
        }

        JSONSerializer().serialize(data)
