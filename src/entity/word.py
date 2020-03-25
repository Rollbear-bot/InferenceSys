# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:26
# @Author: Rollbear
# @Filename: word.py


class Word:
    """文字"""
    def __init__(self, predicate, constant: list):
        """构造方法"""
        self.constant = constant  # 常量, 元组
        self.predicate = predicate  # 谓词, lambda函数

    def __str__(self):
        return self.predicate(self.constant)

    def __eq__(self, other):
        return self.predicate == other.predicate \
               and self.constant == other.constant
