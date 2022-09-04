# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

from distutils.core import setup
from Cython.Build import cythonize


# 程序执行命令: python setup.py build_ext
setup(ext_modules = cythonize(["example/your_codes.py"]))
