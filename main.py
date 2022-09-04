# -*- coding: utf-8 -*-
"""
@Time    : 2022/8/23 13:12
@Author  : itlubber
@Site    : itlubber.art
"""

import sys
sys.path.append("build/lib.macosx-10.9-x86_64-3.8") # 将编译后的包路径添加到python的包路径中


from example.your_codes import itlubber_py2so # 导入需要的包


def read_data(file):
    """
    读取文件中的内容
    """
    with open(file, "r") as f:
        return f.readline()


if __name__ == '__main__':
    msg = read_data("example/README.md") # 读取非 python 文件中的内容
    print(itlubber_py2so(msg)) # 传入文件内容, 打印 itlubber_py2so 返回的结果
