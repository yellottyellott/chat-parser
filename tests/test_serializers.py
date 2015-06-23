from __future__ import unicode_literals

from chat_parser.serializers import JSONSerializer


class TestJSONSerializer(object):
    def test_serializer(self):
        """Verifies the serializer can encode data."""
        data = {
            'mentions': ['jake', 'finny', 'ladyrainicorn'],
            'emoticons': ['breadcrubs', 'thumbsup'],
            'link': [
                {'url': 'lumpyspace.com', 'title': "What the Lump!"},
            ]
        }
        # JSON encoding has non deterministic ordering.
        # Verify the encoder doesn't raise any exceptions
        JSONSerializer().serialize(data)
