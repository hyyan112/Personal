# coding=utf-8
"""
项目结构生成器,使用方法 python structure.py project_path ['ignore_pattern1','ignore_pattern2']
默认忽略'.idea', '.git', 'static', 'tests', 'templates', '.*\.pyc'
"""
import os
import re
import sys


class Builder(object):
    INDENT_STEP = 4  # 每次缩进的空格数
    FORMAT = '| {} '

    def __init__(self, indent=0, layer=1, ignore=None):
        self.indent = indent  # 当前缩进
        self.lines = []  # 保存一行一行生成的代码
        self.layer = layer
        self.ignore = ['.idea', '.git', 'static', 'tests', 'templates', '.*\.pyc']
        if ignore:
            self.ignore.extend(ignore)
        self.ignore_pattern = re.compile('|'.join(self.ignore))

    def forward(self):
        """缩进前进一步"""
        self.indent += self.INDENT_STEP
        self.layer += 1

    def backward(self):
        """缩进后退一步"""
        self.indent -= self.INDENT_STEP
        self.layer -= 1

    def add(self, name):
        self.lines.append(name)

    def add_line(self, name):
        self.lines.append(' ' * self.indent + self.FORMAT.format(self.layer * '-') + name)

    def __str__(self):
        """拼接所有代码行后的源码"""
        return '\n'.join(map(str, self.lines))

    def __repr__(self):
        """方便调试"""
        return str(self)

    def build(self, path):
        name = path.split('/')[-1]
        if self.ignore_pattern.match(name):
            return
        filelist = os.listdir(path)
        for i in filelist:
            if self.ignore_pattern.match(i):
                continue
            self.add_line(i)
            inner = os.path.join(path, i)
            if os.path.isdir(inner):
                self.forward()
                self.build(inner)
        if self.layer > 1:
            self.backward()

    @property
    def result(self):
        return self.__str__()


def generate(path, ignore=None):
    builder = Builder(ignore=ignore)
    builder.build(path)
    print(builder.result)


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2:])
