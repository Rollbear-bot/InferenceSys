# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:26
# @Author: Rollbear
# @Filename: word.py
# 包含"谓词", "文字", 变元对象"Anyone"的声明


class Word:
    """文字"""
    def __init__(self, predicate, constant: list):
        """
        构造方法
        :param predicate: 谓词对象
        :param constant: 常量列表，也可以包含Anyone变元对象
        """
        self.constant = constant  # 常量，也能存放变量Anyone对象
        self.pred = predicate  # 谓词

    def __str__(self):
        return self.pred.func([str(c) for c in self.constant])

    def is_equal(self, other):
        """
        判断两个文字是否相等
        :param other: 另一个文字对象
        :return: 布尔值
        """
        if other is None:
            return False
        if len(self.constant) != len(other.constant):
            return False
        # 首先判断谓词操作的常量是否相同
        for i in range(len(self.constant)):
            # Anyone对象可以匹配任何值
            if self.constant[i] != other.constant[i]:
                return False
        # 最后判断谓词是否相等
        # todo::变量的命名是否合理？
        self_pred_only = self.pred.exec([Anyone("A") for c in range(len(self.constant))])
        other_pred_only = other.pred.exec([Anyone("A") for c in range(len(other.constant))])
        return str(self_pred_only) == str(other_pred_only)

    def copy(self):
        """文字的深复制"""
        return Word(self.pred, self.constant.copy())


class Predicate:
    """谓词"""
    def __init__(self, lambda_func):
        """
        构造方法
        :param lambda_func: 一个函数地址，可以用lambda定义
        """
        self.func = lambda_func

    def exec(self, p: list):
        """
        执行谓词，将谓词和指定的参数组合成一个文字对象
        :param p: 参数
        :return: 文字对象
        """
        return Word(self, p)

    @staticmethod
    def create_pred(info: str):
        """快速建立谓词
        返回(<para1>, <para2>, ...)是<info>形式的谓词"""
        return Predicate(lambda x: "(" + (", ".join(x)) + ")" + "是" + info)

    @staticmethod
    def create_preds(info_lt: list):
        """快速建立一组谓词
        返回(<para1>, <para2>, ...)是<info>形式的谓词组成的元组"""
        return tuple([Predicate.create_pred(info) for info in info_lt])


class Anyone:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"<变量{self.name}>"

    def __eq__(self, other):
        # 如果右操作数不是Anyone实例，则判等始终为真
        if not isinstance(other, Anyone):
            return True
        # 如果是Anyone实例，则要判断变量名是否相等
        else:
            return self.name == other.name
