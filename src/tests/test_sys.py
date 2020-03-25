# -*- coding: utf-8 -*-
# @Time: 2020/3/25 21:31
# @Author: Rollbear
# @Filename: test_sys.py

import unittest

from entity.word import Anyone, Predicate
from entity.horn_clause import HornClause
from entity.system import System
from entity.tree import Node
# from entity.word import Word


class TestSys(unittest.TestCase):
    """测试推理系统"""
    def test_union(self):
        """测试两个子句归结"""
        # 定义谓词
        ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
        win = Predicate(lambda x: str(x[0]) + "中奖")
        study = Predicate(lambda x: str(x[0]) + "学习")
        happy = Predicate(lambda x: str(x[0]) + "快乐")
        lucky = Predicate(lambda x: str(x[0]) + "幸运")

        # 规则集
        r1 = HornClause(happy.exec([Anyone()]),
                        [
                            ps.exec([Anyone(), "历史考试"]),
                            win.exec([Anyone()])
                         ])
        r2 = HornClause(ps.exec([Anyone(), Anyone()]),
                        [
                            study.exec([Anyone()])
                        ])
        r3 = HornClause(ps.exec([Anyone(), Anyone()]),
                        [
                            lucky.exec([Anyone()])
                        ])
        r4 = HornClause(win.exec([Anyone()]),
                        [
                            lucky.exec([Anyone()])
                        ])

        # 事实集
        f1 = HornClause(lucky.exec(["John"]), [None])
        f2 = HornClause(None, [study.exec(["John"])])

        # 待证明结论
        t = HornClause(None, [happy.exec(["John"])])

        # 将上面的霍恩子句加入推理系统
        sys = System(t)
        sys.add_facts([f1, f2])
        sys.add_rules([r1, r2, r3, r4])

        sys.show()


if __name__ == '__main__':
    unittest.main()
