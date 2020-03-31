# -*- coding: utf-8 -*-
# @Time: 2020/3/31 13:24
# @Author: Rollbear
# @Filename: example_of_relatives.py
# 实例：亲属关系推理
from lib.relatives import Relatives
from entity.system import System
from entity.horn_clause import HornClause


def main():
    # 证明目标：Tom和Sally是兄妹关系（不区分年龄）
    # 注：如果更换证明目标后证明失败，先检查库中的规则是否满足证明需求
    t = HornClause(None, [Relatives.bro_sister.exec(["Tom", "Sally"])])

    # 事实集合
    facts_set = [
        # 事实：John和Tom是父子关系
        HornClause(Relatives.father_son.exec(["John", "Tom"]), []),
        # 事实：John和Sally是父女关系
        HornClause(Relatives.father_dau.exec(["John", "Sally"]), [])
    ]

    # 实例化一个证明系统
    sys = System(target=t)

    # 导入上面指定的事实集合
    sys.add_facts(facts=facts_set)

    # 从亲属关系库中导入亲属关系规则
    sys.add_rules(rules=Relatives.get_relatives_rules())

    # 打印系统中现有的所有子句并开始推理
    sys.show()
    res = sys.run(debug=True)
    if res:
        print("证明成功")
    else:
        print("证明失败")


if __name__ == '__main__':
    main()
