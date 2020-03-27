# -*- coding: utf-8 -*-
# @Time: 2020/3/25 21:31
# @Author: Rollbear
# @Filename: test_sys.py
# 单元测试

import unittest

from entity.word import Anyone, Predicate
from entity.horn_clause import HornClause
from entity.system import System
from entity.tree import Node


def create_tmp_horn_clauses():
    """
    创建测试用霍恩子句
    :return: 二元组，两条霍恩子句
    """
    ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
    win = Predicate(lambda x: str(x[0]) + "中奖")
    study = Predicate(lambda x: str(x[0]) + "学习")
    happy = Predicate(lambda x: str(x[0]) + "快乐")
    # 定义子句
    hc1 = HornClause(ps.exec(["John", "历史考试"]), [win.exec(["John"])])
    hc2 = HornClause(None, [ps.exec([Anyone("A"), Anyone("B")])])
    return hc1, hc2


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
        r1 = HornClause(happy.exec([Anyone("A")]),
                        [
                            ps.exec([Anyone("A"), "历史考试"]),
                            win.exec([Anyone("A")])
                         ])
        r2 = HornClause(ps.exec([Anyone("A"), Anyone("B")]),
                        [
                            study.exec([Anyone("A")])
                        ])
        r3 = HornClause(ps.exec([Anyone("A"), Anyone("B")]),
                        [
                            lucky.exec([Anyone("A")])
                        ])
        r4 = HornClause(win.exec([Anyone("A")]),
                        [
                            lucky.exec([Anyone("A")])
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
        res = sys.run()  # 开始推理
        print(res)


class TestWord(unittest.TestCase):
    """测试文字运算"""
    def test_exec(self):
        """测试谓词"""
        # 定义谓词
        ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
        w = ps.exec(["John", "历史考试"])
        self.assertListEqual(w.constant, ["John", "历史考试"])
        self.assertEqual(str(w), "John通过历史考试")


class TestHornClause(unittest.TestCase):
    """测试霍恩子句"""
    def test_define(self):
        hc = create_tmp_horn_clauses()[0]
        self.assertListEqual(hc.head.constant, ["John", "历史考试"])
        self.assertEqual(str(hc), "John通过历史考试 <- John中奖")

    def test_union(self):
        """测试子句消解"""
        hc1, hc2 = create_tmp_horn_clauses()
        hc3 = hc2.union(hc1)
        self.assertEqual(hc3.head, None)
        self.assertEqual(str(hc3.body[0]), "John中奖")

    def test_union_case_2(self):
        """子句消解用例2"""
        happy = Predicate(lambda x: str(x[0]) + "开心")
        ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
        win = Predicate(lambda x: str(x[0]) + "赢得" + str(x[1]))
        hc1 = HornClause(None, [happy.exec(["John"])])
        hc2 = HornClause(
            happy.exec([Anyone("X")]),
            [ps.exec([Anyone("X"), "history"]),
             win.exec([Anyone("X"), "lottery"])])
        result = hc1.union(hc2)
        self.assertListEqual(result.body[0].constant, ["John", "history"])
        self.assertListEqual(result.body[1].constant, ["John", "lottery"])


if __name__ == '__main__':
    unittest.main()
