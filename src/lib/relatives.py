# -*- coding: utf-8 -*-
# @Time: 2020/3/31 13:10
# @Author: Rollbear
# @Filename: relatives.py

from entity.word import Anyone, Predicate
from entity.horn_clause import HornClause


class Relatives:
    """亲属关系"""
    @classmethod
    def get_relatives_rules(cls):
        """获取亲属关系中设置的规则集"""
        return cls._rules_set

    # 谓词定义
    male, female, parenting, father_son, father_dau, \
        mother_son, mother_dau, bro_sister, cousin \
        = Predicate.create_preds(["男性", "女性", "亲子关系",
                                  "父子关系", "父女关系", "母子关系",
                                  "母女关系", "兄妹关系", "表兄妹"])
    # create_preds是简化的批量声明方法，只能声明
    # (<para1>, <para2>, ...)是<info>
    # 形式的谓词

    # 规则集，在这个列表中添加亲属关系所需的规则
    _rules_set = [
        HornClause(female.exec([Anyone("A")]),
                   [father_dau.exec([Anyone("B"), Anyone("A")])]),
        HornClause(male.exec([Anyone("A")]),
                   [father_son.exec([Anyone("B"), Anyone("A")])]),
        HornClause(bro_sister.exec([Anyone("A"), Anyone("B")]),
                   [father_son.exec([Anyone("C"), Anyone("A")]),
                    father_dau.exec([Anyone("C"), Anyone("B")])]),
        HornClause(father_son.exec([Anyone("A"), Anyone("B")]),
                   [bro_sister.exec([Anyone("B"), Anyone("C")]),
                    father_dau.exec([Anyone("A"), Anyone("C")])]),
        HornClause(father_dau.exec([Anyone("A"), Anyone("C")]),
                   [bro_sister.exec([Anyone("B"), Anyone("C")]),
                    father_son.exec([Anyone("A"), Anyone("B")])])
    ]
