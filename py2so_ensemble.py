# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

import os
import sys
import shutil
import argparse
import platform
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension


def getfiles_inpath(dir_path, includeSubfolder=True, path_type=0, ext_names="*"):
    """
        获得指定目录下的所有文件，
        :param dir_path: 指定的目录路径
        :param includeSubfolder: 是否包含子文件夹里的文件，默认 True
        :param path_type: 返回的文件路径形式
            0 绝对路径，默认值
            1 相对路径
            2 文件名
        :param ext_names: "*" | string | list
            可以指定文件扩展名类型，支持以列表形式指定多个扩展名。默认为 "*"，即所有扩展名。
            举例：".txt" 或 [".jpg",".png"]
        :return: 以 yield 方式返回结果
    """
    if type(ext_names) is str:
        if ext_names != "*":
            ext_names = [ext_names]
    if type(ext_names) is list:
        for i in range(len(ext_names)):
            ext_names[i] = ext_names[i].lower()

    def keep_file_byextname(file_name):
        if type(ext_names) is list:
            if file_name[0] == '.':
                file_ext = file_name
            else:
                file_ext = os.path.splitext(file_name)[1]
            #
            if file_ext.lower() not in ext_names:
                return False
        else:
            return True
        return True

    if includeSubfolder:
        len_of_inpath = len(dir_path)
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                if not keep_file_byextname(file_name):
                    continue
                if path_type == 0:
                    yield os.path.join(root, file_name)
                elif path_type == 1:
                    yield os.path.join(
                        root[len_of_inpath:].lstrip(os.path.sep), file_name)
                else:
                    yield file_name
    else:
        for file_name in os.listdir(dir_path):
            filepath = os.path.join(dir_path, file_name)
            if os.path.isfile(filepath):
                if not keep_file_byextname(file_name):
                    continue
                if path_type == 0:
                    yield filepath
                else:
                    yield file_name


def make_dir(dirpath):
    """
    创建目录，支持多级目录，若目录已存在自动忽略
    """
    dirpath = dirpath.strip().rstrip(os.path.sep)

    if dirpath:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


def get_encfile_list(opts):
    will_compile_files = []
    if opts.directory:
        if not os.path.exists(opts.directory):
            print("No such Directory, please check or use the Absolute Path")
            sys.exit(1)

        pyfiles = getfiles_inpath(dir_path=opts.directory,
                                 includeSubfolder=True,
                                 path_type=1,
                                 ext_names='.py')
        # ignore __init__.py file
        pyfiles = [pyfile for pyfile in pyfiles if not pyfile.endswith('__init__.py')]
        # filter maintain files
        opts.excludeFiles = []
        if opts.ignore:
            for path_assign in opts.ignore.split(","):
                if not path_assign[-1:] in ['/', '\\']:  # if last char is not a path sep, consider it's assign a file
                    opts.excludeFiles.append(path_assign)
                else:
                    assign_dir = path_assign.strip('/').strip('\\')
                    tmp_dir = os.path.join(opts.rootName, assign_dir)
                    files = getfiles_inpath(dir_path=tmp_dir,
                                           includeSubfolder=True,
                                           path_type=1)
                    for file in files:
                        fpath = os.path.join(assign_dir, file)
                        opts.excludeFiles.append(fpath)

        tmp_files = list(set(pyfiles) - set(opts.excludeFiles))
        will_compile_files = []
        for file in tmp_files:
            will_compile_files.append(os.path.join(opts.directory, file))

    elif opts.file:
        if opts.file.endswith(".py"):
            will_compile_files.append(opts.file)
        else:
            print("Make sure you give the right name of py file")

    else:
        print("no -f or -d param")
        sys.exit()

    return will_compile_files


def clear_builds(opts):
    if os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.isdir("tmp_build"):
        shutil.rmtree("tmp_build")
    if os.path.isdir(opts.output):
        shutil.rmtree(opts.output)


def clear_tmps(opts):
    if os.path.isdir("build") and opts.output != "build":
        shutil.rmtree("build")
    if os.path.isdir("tmp_build") and opts.output != "tmp_build":
        shutil.rmtree("tmp_build")


def pyencrypt(files):
    extentions = []
    print(files)
    for full_filename in files:
        filename = full_filename[:-3].replace(os.path.sep, '.')
        extention = Extension(filename, [full_filename])
        extention.cython_c_in_temp = True
        extentions.append(extention)
    setup(
        script_args=["build_ext"],
        ext_modules=cythonize(extentions, quiet=False, language_level=3, nthreads=1, build_dir="tmp_build"),
    )


def gen_project(opts, will_compile_files):
    make_dir(opts.output)
    for file in getfiles_inpath('build', True, 1, ['.so', '.pyd']):
        src_path = os.path.join('build', file)
        mid_path = os.path.sep.join(file.split(os.path.sep)[1:-1])
        file_name_parts = os.path.basename(src_path).split('.')
        file_name = '.'.join([file_name_parts[0]] + file_name_parts[-1:])
        dest_path = os.path.join(opts.output, mid_path, file_name)
        make_dir(os.path.dirname(dest_path))
        shutil.copy(src_path, dest_path)
    
    # 非编译文件拷贝至结果路径
    not_compile_files = get_not_compile_files(opts, will_compile_files)
    for not_compile_file in not_compile_files:
        dest_path = os.path.join(opts.output, not_compile_file)
        filepath, filename = os.path.split(dest_path)
        make_dir(filepath)
        shutil.copyfile(not_compile_file, dest_path)

    if opts.remove:
        clear_tmps(opts)
    
    print("py2so encrypt build complate.")


def get_not_compile_files(opts, will_compile_files):
    """
    获取非编译文件
    """
    files = getfiles_inpath(dir_path=opts.directory,
                           includeSubfolder=True,
                           path_type=1,
                           ext_names='*')
    files = [os.path.join(opts.directory, file) for file in files if not file.endswith('.pyc')]
    not_compile_files = list(set(files) - set(will_compile_files))
    return not_compile_files


if __name__ == '__main__':
    # 不支持 windows 系统编译
    if platform.system() == 'Windows':
        print("只支持linux，windows下可以使用pyinstaller打包exe")
        sys.exit()
    
    # 编译参数
    parser = argparse.ArgumentParser(description="py2so options:")
    
    # -d 和 -f 二选一
    exptypegroup = parser.add_mutually_exclusive_group()
    exptypegroup.add_argument("-f", "--file", help="python文件 (如果使用-f, 将编译单个python文件)", default="")
    exptypegroup.add_argument("-d", "--directory", help="python项目路径 (如果使用-d参数, 将编译整个python项目)", default="")
    
    parser.add_argument("-o", "--output", help="编译完成后整个项目输出的文件路径", default="itlubber_py2so")
    parser.add_argument("-i", "--ignore", help="""标记你不想编译的文件或文件夹路径。注意: 文件夹需要以路径分隔符号（`/`或`\\`，依据系统而定）结尾，并且需要和-d参数一起使用。例: -i main.py,mod/__init__.py,exclude_dir/""")
    parser.add_argument("-r", "--remove", help="清除所有中间文件，只保留加密结果文件，默认True", action="store_true", default=True)
    opts = parser.parse_args()
    
    # 获取所有待编译 python 文件
    will_compile_files = get_encfile_list(opts)
    
    # 清空上一次运行生成的临时文件
    clear_builds(opts)
    
    # 编译 python 文件
    pyencrypt(will_compile_files)
    
    # 将编译好的工程输出到结果文件夹
    gen_project(opts, will_compile_files)
