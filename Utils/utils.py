import os

root_path = os.path.dirname(os.path.dirname(__file__))


def load_keywords():
    collector = set()
    for filename in os.listdir(os.path.join(root_path, "keywords")):
        fr = open(os.path.join(root_path, "keywords", filename), "r")
        for line in fr.readlines():
            collector.add(line.strip())
        fr.close()
    return collector


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
