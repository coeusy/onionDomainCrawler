import os

root_path = os.path.dirname(os.path.dirname(__file__))


def load_keywords():
    for filename in os.listdir(os.path.join(root_path, "keywords")):
        fr = open(os.path.join(root_path, "keywords", filename), "r")
        for line in fr.readlines():
            yield line.strip()
        fr.close()
