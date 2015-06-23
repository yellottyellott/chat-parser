import json


class JSONSerializer(object):
    def serialize(self, data):
        return json.dumps(data, indent=2)
