# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:20
# @Author: Rollbear
# @Filename: horn_clause.py
from entity.word import Anyone, Word


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
        # union运算不应该修改操作数本身
        self_clone = self.copy()
        other_clone = other.copy() if other is not None else None

        if not self_clone.body[0].is_equal(other_clone.head):
            raise InvalidOperation

        # 带变量的子句归结：
        # 某个文字的某个谓词是变量->从与其消解的文字中找出对应位置的常量
        # ->定位前者所有文字中的这个变量
        # ->这个变量在这条子句中的所有出现用上面提到的常量取代
        # 首先检查左操作数的负文字是否含有变量
        for index, c in enumerate(self_clone.body[0].constant):
            if isinstance(c, Anyone):
                # 找出对应位置的常量
                map_constant = other_clone.head.constant[index]
                for word in self_clone.body:
                    # 遍历左操作数的所有负文字的所有元
                    for e_index, elem in enumerate(word.constant):
                        if isinstance(elem, Anyone) and elem == c:
                            word.constant[e_index] = map_constant

        # 对右操作数的头部和体部的所有文字，重复上面的检查算法
        for index, c in enumerate(other_clone.head.constant):
            if isinstance(c, Anyone):
                # 找出对应位置的常量
                map_constant = self_clone.body[0].constant[index]
                # 遍历所有元
                for e_index, elem in enumerate(other_clone.head.constant):
                    if isinstance(elem, Anyone) and elem == c:
                        other_clone.head.constant[e_index] = map_constant
                for word in other_clone.body:
                    for e_index, elem in enumerate(word.constant):
                        if isinstance(elem, Anyone) and elem == c:
                            word.constant[e_index] = map_constant

        # 结果是无头子句
        result = HornClause(None, self_clone.body[1:] + other_clone.body)
        return result

    def is_null_clause(self):
        """当前子句是否为空子句"""
        return self.head in [None, []] and set(self.body) in [{None}, set()]

    def copy(self):
        """Horn子句的深复制"""
        return HornClause(self.head.copy() if self.head is not None else None,
                          [word.copy() for word in self.body if word is not None])

    @staticmethod
    def create_clause_variables_only(head: tuple, body: tuple):
        """
        快速建立只含变量的子句
        :param head: 格式(predicate,[var_names...])的元组
        :param body: 格式(predicate,[var_names...])的元组组成的元组
        :return: Horn子句
        """
        return HornClause(head[0].exec([Anyone(var_name) for var_name in head[1]]),
                          [word[0].exec(Anyone(var_name) for var_name in word[1]) for word in body])
