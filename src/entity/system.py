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

    def add_rules(self, rules: list):
        """批量添加规则"""
        for r in rules:
            self.add_rule(r)

    def add_fact(self, fact: HornClause):
        """向事实库中添加事实"""
        if not isinstance(fact, HornClause):
            raise UnexpectedObj
        # 事实库中必须是无头/无体子句
        if not (fact.body[0] is None or fact.head is None):
            raise UnexpectedObj
        self.facts.append(fact)

    def add_facts(self, facts):
        """批量添加事实"""
        for f in facts:
            self.add_fact(f)

    def show(self):
        """打印推理系统中的子句"""
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
        root = Node(self.target)  # 从推理目标开始
        return self.s_recursion(root, repo)

    def s_recursion(self, cur_node: Node, cur_repo: list):
        """
        递归归结
        :param cur_node: 当前结点
        :param cur_repo: 当前子句仓库
        :return: 空子句或异常
        """
        if cur_node.data.is_null_clause():
            return cur_node.data  # 如果当前已到达空子句则返回，递归出口

        # 从库中筛选所有正文字与当前节点“左边第一个负文字”相等的子句
        clauses_has_head = list(filter(lambda x: x.head is not None, cur_repo))
        target_lt = list(filter(lambda x: x.head.is_equal(cur_node.data.body[0]), clauses_has_head))
        # 若找不到匹配的子句，说明证明条件不充分，算法结束
        if len(target_lt) == 0:
            raise InferenceFail
        # 对lt中的每一个选择都建立一个分支
        for t in target_lt:
            # 两个子句消解
            new_clause = cur_node.data.union(t)
            # 新子句作为子节点链入树中
            cur_node.sub_node.append(Node(new_clause))
            # 新子句加入库
            cur_repo.append(new_clause)
        # 检查是否所有分支的终点都是空子句
        for sub in cur_node.sub_node:
            if not self.s_recursion(sub, cur_repo).is_null_clause():
                raise InferenceFail
        return HornClause(None, [None])


class UnexpectedObj(Exception):
    """传入了不正确的对象"""

    def __str__(self):
        return "传入了不正确的对象"


class InferenceFail(Exception):
    def __str__(self):
        return "推理失败"
