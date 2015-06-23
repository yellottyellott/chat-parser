from . import parsers
from . import serializers


class Handler(object):
    parser_classes = {
        'mentions': parsers.MentionParser,
        'emoticons': parsers.EmoticonParser,
        'links': parsers.LinkParser,
    }

    serializer_class = serializers.JSONSerializer

    def parse(self, string):
        data = {}
        for key, cls in self.parser_classes.iteritems():
            parser = cls()
            matches = parser.parse(string)
            if matches:
                data[key] = matches

        return data

    def serialize(self, data):
        serializer = self.serializer_class()
        return serializer.serialize(data)


def parse(string, format='json'):
    handler = Handler()
    return handler.serialize(handler.parse(string))
