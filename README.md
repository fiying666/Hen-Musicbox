# 🐔音盒

一个基于[PYWEBIO](https://github.com/pywebio/PyWebIO) 的趣味音频播放软件

## 本地运行

### 环境

1. [Python](https://www.python.org/) >= 3.8
2. PyWebIO
3. playsound
4. keyboard

pip安装（清华源镜像）

```shell
pip install pywebio playsound keyboard -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 打包为EXE文件

参考PyWebIO官方文档：[构建stand-alone App](https://pywebio.readthedocs.io/zh_CN/latest/libraries_support.html#build-stand-alone-app)


**1. 安装Pyinstaller**

```shell
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**2. 创建pyinstaller spec (specification) 文件**

```shell
pyi-makespec --onefile main.py
```

**3. 编辑生成的spec文件，在第二行添加内容，并将其中 Analysis 的 data 参数修改为**

```py
from pywebio.utils import pyinstaller_datas

a = Analysis(
    ...
    datas=pyinstaller_datas(),
    ...
```

**4. 使用spec文件来构建可执行文件**

```shell
pyinstaller -w main.spec
```

`-w` 参数：取消显示命令行窗口

> **音频资源来源于互联网，若有侵权请及时联系删除**
