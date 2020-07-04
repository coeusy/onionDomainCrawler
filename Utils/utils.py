import os

root_path = os.path.dirname(os.path.dirname(__file__))


def load_keywords():
    for filename in os.listdir(os.path.join(root_path, "keywords")):
        fr = open(os.path.join(root_path, "keywords", filename), "r")
        for line in fr.readlines():
            yield line.strip()
        fr.close()


# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
