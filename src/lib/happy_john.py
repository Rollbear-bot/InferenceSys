# -*- coding: utf-8 -*-
# @Time: 2020/3/31 13:25
# @Author: Rollbear
# @Filename: example_of_happy_john.py
# happy John 例子中的谓词和规则
from entity.word import Predicate, Anyone
from entity.horn_clause import HornClause


class HappyJohn:
    @classmethod
    def get_rules_set(cls):
        """获取Happy John例子中设置的规则"""
        return cls._rules_set

    # 定义谓词
    ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
    win = Predicate(lambda x: str(x[0]) + "中奖")
    study = Predicate(lambda x: str(x[0]) + "学习")
    happy = Predicate(lambda x: str(x[0]) + "快乐")
    lucky = Predicate(lambda x: str(x[0]) + "幸运")

    # 规则集
    _rules_set = [
        HornClause(happy.exec([Anyone("A")]),
                   [ps.exec([Anyone("A"), "历史考试"]),
                    win.exec([Anyone("A")])]),
        HornClause(ps.exec([Anyone("A"), Anyone("B")]),
                   [study.exec([Anyone("A")])]),
        HornClause(ps.exec([Anyone("A"), Anyone("B")]),
                   [lucky.exec([Anyone("A")])]),
        HornClause(win.exec([Anyone("A")]),
                   [lucky.exec([Anyone("A")])]),
    ]
