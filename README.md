# py2so

本仓库从易到难，简单梳理了.so文件编译的几种方案：最原始的编译方法、不删除中间文件的编译方法和相对集成的编译方案。推荐直接食用第三种集成方案，个人目前使用第二种。

> 博客文章地址: https://itlubber.art/archives/python-py2so
> 微信公众号文章地址: https://mp.weixin.qq.com/s/LgDwJGl34ew3qgLXSJrIuA


## 项目结构

```
$ tree
.
├── LICENSE                     # 项目 MIT 协议
├── README.md                   # 说明文档
├── clear_cache.sh              # 自用清除缓存的脚本
├── example                     # 示例项目
│   ├── README.md               # 示例非python文件
│   ├── __init__.py
│   └── your_codes.py           # 示例python文件
├── main.py                     # 示例项目主程序脚本
├── py2so.py                    # 半集成方案，自用且推荐
├── py2so_ensemble.py           # 集成方案，推荐
└── setup.py                    # 原始编译方法

1 directory, 10 files
```

## 原始编译方法: [`setup.py`](https://github.com/itlubber/py2so/blob/main/setup.py)

在代码中修改需要编译的文件即可，会生成中间文件

## 半集成方法: [`py2so.py`](https://github.com/itlubber/py2so/blob/main/py2so.py)

使用时放在项目主程序文件同级目录，例如本项目中需要将 `py2so.py` 放置于 `main.py` 所在的目录（即同级目录），然后运行编译脚本 `python py2so.py` 即可，编译完成后所有项目文件都存放在 `./build` 目录下方

## 集成方法: [`py2so_ensemble.py`](https://github.com/itlubber/py2so/blob/main/py2so_ensemble.py)

使用时放在项目主程序文件上级目录，例如本项目中需要将 `py2so_ensemble.py` 放置于 `main.py` 所在的目录外（即上级目录），然后运行编译脚本 `python py2so_ensemble.py -d py2so` 即可，编译完成后所有项目文件都默认存放在 `./itlubber_py2so` 目录下方
