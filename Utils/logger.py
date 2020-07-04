import logging
import os
from .utils import singleton


@singleton
class Log:

    def __init__(self, name=None):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        file_dir = os.path.dirname(__file__) + '/../log'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, "error.log")

        fh = logging.FileHandler(file_path, 'a')
        fh.setLevel(logging.ERROR)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s:%(lineno)d %(process)d.%(thread)d [%(levelname)s]%(message)s ')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        fh.close()
        ch.close()

    def get_log(self):
        return self.logger

