# -*- coding: utf-8 -*-
# @Time: 2020/3/25 21:31
# @Author: Rollbear
# @Filename: test_sys.py
# 单元测试

import unittest

from entity.word import Anyone, Predicate
from entity.horn_clause import HornClause
from entity.system import System


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
    def test_system(self):
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
        f1 = HornClause(lucky.exec(["John"]), [])
        f2 = HornClause(None, [study.exec(["John"])])

        # 待证明结论
        t = HornClause(None, [happy.exec(["John"])])

        # 将上面的霍恩子句加入推理系统
        sys = System(t)
        sys.add_facts([f1, f2])
        sys.add_rules([r1, r2, r3, r4])
        self.assertTrue(sys.run())

    def test_system_case_2(self):
        """测试亲戚关系运算"""
        # 定义谓词
        male, female, parenting, father_son, father_dau, \
            mother_son, mother_dau, bro_sister, cousin \
            = Predicate.create_preds(["男性", "女性", "亲子关系",
                                      "父子关系", "父女关系", "母子关系",
                                      "母女关系", "兄妹关系", "表兄妹"])

        # 事实集合
        f1 = HornClause(father_son.exec(["John", "Tom"]), [])
        f2 = HornClause(father_dau.exec(["John", "Sally"]), [])

        # 规则集合
        r1 = HornClause(female.exec([Anyone("A")]),
                        [father_dau.exec([Anyone("B"), Anyone("A")])])
        r2 = HornClause(male.exec([Anyone("A")]),
                        [father_son.exec([Anyone("B"), Anyone("A")])])
        r3 = HornClause(bro_sister.exec([Anyone("A"), Anyone("B")]),
                        [father_son.exec([Anyone("C"), Anyone("A")]),
                         father_dau.exec([Anyone("C"), Anyone("B")])])
        r4 = HornClause(father_son.exec([Anyone("A"), Anyone("B")]),
                        [bro_sister.exec([Anyone("B"), Anyone("C")]),
                         father_dau.exec([Anyone("A"), Anyone("C")])])
        r5 = HornClause(father_dau.exec([Anyone("A"), Anyone("C")]),
                        [bro_sister.exec([Anyone("B"), Anyone("C")]),
                         father_son.exec([Anyone("A"), Anyone("B")])])

        # 推理目标
        target = HornClause(None, [bro_sister.exec(["Tom", "Sally"])])

        sys = System(target)
        sys.add_facts([f1, f2])
        sys.add_rules([r1, r2, r3, r4, r5])
        self.assertTrue(sys.run())


class TestWord(unittest.TestCase):
    """测试文字运算"""
    def test_exec(self):
        """测试谓词"""
        # 定义谓词
        ps = Predicate(lambda x: str(x[0]) + "通过" + str(x[1]))
        w = ps.exec(["John", "历史考试"])
        self.assertListEqual(w.constant, ["John", "历史考试"])
        self.assertEqual(str(w), "John通过历史考试")

    def test_create_pred(self):
        """测试快速建立谓词方法create_pred"""
        father_son = Predicate.create_pred("父子关系")
        word = father_son.exec(["A", "B"])
        self.assertEqual(str(word), "(A, B)是父子关系")


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

    def test_quick_build(self):
        """快速建立只含变量的子句"""
        male = Predicate.create_pred("男性")
        female = Predicate.create_pred("女性")
        body = ((male, ["A"]), (female, ["B"]))
        c = HornClause.create_clause_variables_only((male, ["A"]), body)
        self.assertEqual(str(c), "(<变量A>)是男性 <- (<变量A>)是男性, (<变量B>)是女性")


if __name__ == '__main__':
    unittest.main()
