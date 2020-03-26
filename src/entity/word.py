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
        other_c = other.constant.copy()
        self_c = self.constant.copy()
        if len(self.constant) != len(other.constant):
            return False
        for i in range(len(self.constant)):
            if self.constant[i] != other.constant[i]:
                if self.constant[i] == Anyone() \
                        or other.constant[i] == Anyone():
                    # Anyone对象可以匹配任何值
                    other_c[i], self_c[i] = Anyone()
                    pass
                else:
                    return False
        return str(Word(self.pred, self_c)) == str(Word(other.pred, other_c))


class Predicate:
    """谓词"""
    def __init__(self, lambda_func):
        self.func = lambda_func

    def exec(self, p: list):
        """
        执行谓词
        :param p: 参数
        :return: 字符串
        """
        # return self.func(p)
        return Word(self, p)


class Anyone:
    def __str__(self):
        return "<任何>"

    def __eq__(self, other):
        return True
