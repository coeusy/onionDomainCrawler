import os

root_path = os.path.dirname(os.path.dirname(__file__))


def load_keywords():
    keywords = set()
    for filename in os.listdir(os.path.join(root_path, "keywords")):
        fr = open(os.path.join(root_path, "keywords", filename), "r")
        for line in fr.readlines():
            keywords.add(line.strip())
        fr.close()
    return keywords


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
