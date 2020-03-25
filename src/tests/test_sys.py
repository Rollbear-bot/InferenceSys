# -*- coding: utf-8 -*-
# @Time: 2020/3/25 21:31
# @Author: Rollbear
# @Filename: test_sys.py

import unittest

from entity.word import Word
from entity.horn_clause import HornClause
from entity.system import System
from entity.tree import Node
from entity.word import Word


class TestSys(unittest.TestCase):
    """测试推理系统"""
    def test_union(self):
        """测试两个子句归结"""
        w1 = Word(lambda x: x[0] + "会飞", ["鸟"])
        w2 = Word(lambda x: x[0] + "喜欢" + x[1], ["A", "B"])
        w3 = Word(lambda x: x[0] + "会游", ["鱼"])
        w4 = Word(lambda x: x[0] + "会跑", ["马"])
        w5 = Word(lambda x: x[0] + "会跳", ["兔子"])

        print(w1)
        print(w2)


        r1 = HornClause(head=w1, body=[w2, w3])
        r2 = HornClause(None, body=[w1])
        target = HornClause(None, [w4])
        sys = System(target)
        sys.add_fact(r2)
        sys.add_rule(r1)
        sys.show()


if __name__ == '__main__':
    unittest.main()
