from distutils.core import setup
from Cython.Build import cythonize


# 程序执行命令: python setup.py build_ext
setup(ext_modules = cythonize(["example/your_codes.py"]))
