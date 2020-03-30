# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:20
# @Author: Rollbear
# @Filename: horn_clause.py

from .word import Word, Anyone


class InvalidOperation(Exception):
    def __str__(self):
        return "无效运算"


class HornClause:
    """Horn子句"""
    def __init__(self, head: Word, body: list):
        """构造方法"""
        self.head = head
        self.body = body

    def __str__(self):
        return str(self.head) + " <- " \
               + ", ".join([str(i) for i in self.body])

    def union(self, other):
        """
        两个子句消解，左操作数是无头子句
        :param other: 另一个子句
        :return: 新的子句（消解结果）
        """
        if not self.body[0].is_equal(other.head):
            raise InvalidOperation

        # 如果一个文字中有Anyone变量，而另一子句的相应文字是常量，
        # 则应当用常量取代变量
        # todo::常量替换对一个子句中的同一个变量应当同时替换
        for c in self.body[0].constant:
            if isinstance(c, Anyone):
                self.body[0].constant = other.head.constant
        for c in other.head.constant:
            if isinstance(c, Anyone):
                other.head.constant = self.body[0].constant

        # 结果是无头子句
        result = HornClause(None, self.body[1:] + other.body)
        return result

    def is_null_clause(self):
        """当前子句是否为空子句"""
        return self.head is None and set(self.body) == {None}

    @staticmethod
    def create_clause_variables_only(head: list, body: list):
        """
        快速建立只含变量的子句
        :param head: 格式(predicate,[var_names...])的元组
        :param body: 格式(predicate,[var_names...])的元组组成的列表/元组
        :return: Horn子句
        """
        return HornClause(head[0].exec([Anyone(var_name) for var_name in head[1]]),
                          [word[0].exec(Anyone(var_name) for var_name in word[1]) for word in body])
