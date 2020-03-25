# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:31
# @Author: Rollbear
# @Filename: test.py

from entity.word import Word
from entity.horn_clause import HornClause
from entity.system import System
from entity.tree import Node
from entity.word import Word


def main():
    w1 = Word(lambda x: str(x) + "会飞", tuple("鸟"))
    w2 = Word(lambda x: str(x) + "会叫", tuple("狗"))
    w3 = Word(lambda x: str(x) + "会游", tuple("鱼"))
    w4 = Word(lambda x: str(x) + "会跑", tuple("马"))
    w5 = Word(lambda x: str(x) + "兔子", tuple("会跳"))

    r1 = HornClause(head=w1, body=[w2, w3])
    r2 = HornClause(None, body=[w1])
    target = HornClause(None, [w4])
    sys = System(target)
    sys.add_fact(r2)
    sys.add_rule(r1)
    sys.show()
    # print(r1)


if __name__ == '__main__':
    main()
