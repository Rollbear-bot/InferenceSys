# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:20
# @Author: Rollbear
# @Filename: horn_clause.py

from .word import Word


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
        两个子句消解
        :param other: 另一个子句
        :return: 新的子句（消解结果）
        """
        if self.body[0] != other.head:
            raise InvalidOperation
        # 结果是无头子句
        result = HornClause(None, self.body[1:] + other.body)
        return result

    def is_null_clause(self):
        """当前子句是否为空子句"""
        return self.head is None and self.body == [None]
