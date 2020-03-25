# -*- coding: utf-8 -*-
# @Time: 2020/3/25 20:19
# @Author: Rollbear
# @Filename: tree.py


class Node:
    """树节点"""
    def __init__(self, data):
        """构造方法"""
        self.sub_node = []  # 子节点
        self.parent = None  # 父节点
        self.data = data  # 数据域
