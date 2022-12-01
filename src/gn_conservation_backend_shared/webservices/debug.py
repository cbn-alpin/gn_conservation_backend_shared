import json


def fprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))
