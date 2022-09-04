# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

import os
import sys
import time
import shutil
from distutils.core import setup
from Cython.Build import cythonize


currdir = os.path.abspath('.')
build_dir = "build"
build_tmp_dir = build_dir + "/temp"


def getpy(basepath, name='', excepts=[], copyOther=False, delC=False, starttime=None):
    """
    获取py文件的路径
    :param basepath: 根路径
    :param name: 文件/夹
    :param copy: 是否copy其他文件
    :param excepts: 不拷贝的文件
    :return: py文件的迭代器
    """
    excepts_files = [os.path.join(currdir, f) for f in excepts]
    fullpath = os.path.join(basepath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        
        if os.path.isdir(ffile) and fname != build_dir and not fname.startswith('.'):
            for f in getpy(basepath, name=fname, copyOther=copyOther, delC=delC, starttime=starttime):
                yield f
                
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext == ".c":
                if delC and os.stat(ffile).st_mtime > starttime:
                    os.remove(ffile)
            elif os.path.splitext(fname)[1] not in('.pyc', '.pyx'):
                if os.path.splitext(fname)[1] in ('.py', '.pyx') and not fname.startswith('__'):
                    yield os.path.join(name, fname)
                elif ffile not in excepts_files and copyOther:
                    dstdir = os.path.join(basepath, build_dir, name)
                    if not os.path.isdir(dstdir):
                        os.makedirs(dstdir)
                    shutil.copyfile(ffile, os.path.join(dstdir, fname))
        else:
            pass
        
        
def copy_file(source):
    dist_dir = os.path.join(currdir, build_dir, source)
    source_dir = os.path.join(currdir, source)
    
    if not os.path.isdir(source_dir):
        if not os.path.exists(os.path.dirname(dist_dir)):
            os.makedirs(os.path.dirname(dist_dir))
    
        shutil.copyfile(source_dir, dist_dir)
    else:
        for file in os.listdir(source_dir):
            copy_file(os.path.join(source_dir, file))


if __name__ == '__main__':
    starttime=time.time()
    
    # 不编译的 python 文件
    excepts_build = ["py2so.py", "main.py"]
    # 不复制到编译后的非 python 文件
    excepts_files = ["README.md", "LICENSE", ".gitignore", "setup.py"]

    # 编译 python 文件
    module_list = list(getpy(currdir, starttime=starttime))
    module_list = [py for py in module_list if py not in excepts_build]
    setup(ext_modules = cythonize(module_list), script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])

    # 拷贝其他文件
    list(getpy(currdir, excepts=excepts_files, copyOther=True, starttime=starttime))
    
    # 拷贝不编译的py文件
    for file in excepts_build:
        copy_file(file)

    # 删除编译产生的中间文件
    module_list = list(getpy(currdir, delC=True, starttime=starttime))
    if os.path.exists(build_tmp_dir):
        shutil.rmtree(build_tmp_dir)

    print ("complate! time:", time.time()-starttime, 's')
