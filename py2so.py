import os
import shutil
import sys
import time
from distutils.core import setup
from Cython.Build import cythonize


starttime = time.time()
currdir = os.path.abspath('.')
parentpath = sys.argv[1] if len(sys.argv)>1 else ""
setupfile= os.path.join(os.path.abspath('.'), __file__)
build_dir = "build"
build_tmp_dir = build_dir + "/temp"


def getpy(basepath=os.path.abspath('.'), parentpath='', name='', excepts=(), copyOther=False,delC=False):
    """
    获取py文件的路径
    :param basepath: 根路径
    :param parentpath: 父路径
    :param name: 文件/夹
    :param excepts: 排除文件
    :param copy: 是否copy其他文件
    :return: py文件的迭代器
    """
    fullpath = os.path.join(basepath, parentpath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        if os.path.isdir(ffile) and fname != build_dir and not fname.startswith('.'):
            for f in getpy(basepath, os.path.join(parentpath, name), fname, excepts, copyOther, delC):
                if f not in excepts:
                    yield f
                else:
                    pass
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext == ".c":
                if delC and os.stat(ffile).st_mtime > starttime:
                    os.remove(ffile)
            elif ffile not in excepts and os.path.splitext(fname)[1] not in('.pyc', '.pyx'):
                if os.path.splitext(fname)[1] in('.py', '.pyx') and not fname.startswith('__'):
                    yield os.path.join(parentpath, name, fname)
                elif copyOther:
                        dstdir = os.path.join(basepath, build_dir, parentpath, name)
                        if not os.path.isdir(dstdir): 
                            os.makedirs(dstdir)
                        shutil.copyfile(ffile, os.path.join(dstdir, fname))
        else:
            pass


if __name__ == '__main__':
    excepts_file = (setupfile)

    # 编译 .py 文件
    try:
        module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=excepts_file))
        setup(ext_modules = cythonize(module_list),script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])
    except Exception as e:
        print (e)

    # 拷贝其他文件
    list(getpy(basepath=currdir, parentpath=parentpath, excepts=excepts_file, copyOther=True))

    # 删除编译产生的中间文件
    module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=excepts_file, delC=True))
    if os.path.exists(build_tmp_dir):
        shutil.rmtree(build_tmp_dir)

    print ("complate! time:", time.time()-starttime, 's')
