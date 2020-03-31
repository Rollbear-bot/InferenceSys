# -*- coding: utf-8 -*-
# @Time: 2020/3/31 13:23
# @Author: Rollbear
# @Filename: example_of_happy_john.py
# 示例：快乐的John
from lib.happy_john import HappyJohn
from entity.system import System
from entity.horn_clause import HornClause


def main():
    # 声明证明目标子句，"happy"是HappyJohn库中声明的谓词对象
    # 证明目标：子句"None <- John快乐"，
    # 在子句对象输出时使用None占位，表示某个位置空
    # 注：如果更换证明目标后证明失败，先检查库中的规则是否满足证明需求
    t = HornClause(None, [HappyJohn.happy.exec(["John"])])

    # 事实集
    facts_set = [
        # 子句"John快乐 <- None"，这里的lucky是HappyJohn库中声明的谓词对象
        HornClause(HappyJohn.lucky.exec(["John"]), []),
        # 子句"None <- John学习"
        HornClause(None, [HappyJohn.study.exec(["John"])])
    ]

    # 实例化一个证明系统
    sys = System(target=t)

    # 向系统中添加规则和事实集
    # 将HappyJohn库中设置的规则引入
    sys.add_rules(rules=HappyJohn.get_rules_set())
    sys.add_facts(facts=facts_set)

    # 打印推理系统中现有的所有子句
    sys.show()

    # 开始推理，参数debug指定是否将推理过程打印到控制台
    # run方法返回一个布尔值，表示推理是否成功
    res = sys.run(debug=True)
    if res:
        print("证明成功")
    else:
        print("证明失败")


if __name__ == '__main__':
    main()
