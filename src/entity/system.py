# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:22
# @Author: Rollbear
# @Filename: system.py

from .horn_clause import HornClause
from .tree import Node


class System:
    """推理系统"""
    def __init__(self, target: HornClause):
        """构造方法"""
        self.rules = []  # 规则集
        self.facts = []  # 事实集
        self.target = target  # 证明目标

    def add_rule(self, rule: HornClause):
        """向规则库中添加规则"""
        if not isinstance(rule, HornClause):
            raise UnexpectedObj
        self.rules.append(rule)

    def add_fact(self, fact: HornClause):
        """向事实库中添加事实"""
        if not isinstance(fact, HornClause):
            raise UnexpectedObj
        # 事实库中必须是无头/无体子句
        if not (fact.body is None or fact.head is None):
            raise UnexpectedObj
        self.facts.append(fact)

    def show(self):
        print("# 事实")
        for fact in self.facts:
            print(fact)
        print("\n# 规则")
        for rule in self.rules:
            print(rule)
        print("\n# 目标\n" + str(self.target))

    def simplify(self):
        """归结"""
        repo = self.rules + self.facts  # 把规则和事实合成一个库
        root = Node(self.target)
        cur_node = root
        # 在库中寻找能够归结的子句
        while cur_node is not None:
            target = filter(lambda x: x.head == cur_node.data.body[0], repo)




class UnexpectedObj(Exception):
    """传入了不正确的对象"""
    def __str__(self):
        return """传入了不正确的对象"""

