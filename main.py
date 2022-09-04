# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

from example.your_codes import py2so_code


def read_data(file):
    with open(file, "r") as f:
        return f.readline()


if __name__ == '__main__':
    file = "example/README.md"
    msg = read_data(file)
    print(py2so_code(msg))
