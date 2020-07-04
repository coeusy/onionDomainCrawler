import os
from configparser import *
from .utils import singleton
from collections import defaultdict


@singleton
class ConfigLoader:

    def __init__(self):
        self.dir = os.path.join(os.path.dirname(__file__), '../conf')
        self.config_dict = {}
        self.ins_dict = {}
        self.load_all()

    # Load all config files in a dict
    def load_all(self):
        files = os.listdir(self.dir)
        for file in files:
            self.load(file)

    def load(self, src_path):
        path, file = os.path.split(src_path)
        k, ext = file.split('.')
        if ext == 'cfg':
            cfg_parser = ConfigParser()
            cfg_parser.read(os.path.join(self.dir, file))
            self.config_dict[k] = self.convert_to_dict(cfg_parser)

    @staticmethod
    def convert_to_dict(cfg_parser):
        res = defaultdict(dict)
        for section in cfg_parser.sections():
            for it in cfg_parser.items(section):
                try:
                    res[section][it[0]] = int(it[1])
                except ValueError:
                    res[section][it[0]] = it[1]
        return res
