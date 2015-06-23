from . import matchers
from . import serializers


class Handler(object):
    matcher_classes = {
        'mentions': matchers.MentionMatcher,
        'emoticons': matchers.EmoticonMatcher,
        'links': matchers.LinkMatcher,
    }

    serializer_class = serializers.JSONSerializer

    def parse(self, string):
        data = {}
        for key, cls in self.matcher_classes.iteritems():
            matcher = cls()
            matches = matcher.matches(string)
            if matches:
                data[key] = matches

        return data

    def serialize(self, data):
        serializer = self.serializer_class()
        return serializer.serialize(data)


def parse(string, format='json'):
    handler = Handler()
    return handler.serialize(handler.parse(string))
