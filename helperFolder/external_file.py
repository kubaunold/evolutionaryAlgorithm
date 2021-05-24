# external_file.py

import logging

p = logging.getLogger(__name__)
p.setLevel(logging.INFO)


def test():
    p.info(__name__)


if __name__ == "__main__":
    test()