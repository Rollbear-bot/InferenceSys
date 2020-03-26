# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:26
# @Author: Rollbear
# @Filename: word.py


class Word:
    """文字"""
    def __init__(self, predicate, constant: list):
        """构造方法"""
        self.constant = constant  # 常量
        self.pred = predicate  # 谓词

    def __str__(self):
        return self.pred.func(self.constant)

    def is_equal(self, other):
        """判断两个文字是否相等"""
        if len(self.constant) != len(other.constant):
            return False
        # 首先判断谓词操作的常量是否相同
        for i in range(len(self.constant)):
            # Anyone对象可以匹配任何值
            if self.constant[i] != other.constant[i]:
                return False
        # 最后判断谓词是否相等
        self_pred_only = self.pred.exec([Anyone() for c in range(len(self.constant))])
        other_pred_only = other.pred.exec([Anyone() for c in range(len(other.constant))])
        return str(self_pred_only) == str(other_pred_only)


class Predicate:
    """谓词"""
    def __init__(self, lambda_func):
        self.func = lambda_func

    def exec(self, p: list):
        """
        执行谓词
        :param p: 参数
        :return: 文字对象
        """
        return Word(self, p)


class Anyone:
    def __str__(self):
        return "<任何>"

    def __eq__(self, other):
        return True
