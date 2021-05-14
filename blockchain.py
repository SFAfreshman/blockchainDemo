# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:44:30 2021

@author: Lenovo
"""

from basic import Base
class Block(Base):
    def __init__(self, prev_hash: str = None):
        self.items = []
        self.prev_hash = prev_hash

    def add(self, item):
        item.prev_hash = self.items[-1].hash() if len(self.items) else None
        self.items.append(item)

    def validate(self):
        for i in range(len(self.items)):
            assert i == 0 or self.items[i].prev_hash == self.items[i - 1].hash()


class Blockchain(Base):
    def __init__(self):
        self.blocks = []

    def add(self, block):
        block.prev_hash = self.blocks[-1].hash() if len(self.blocks) else None
        self.blocks.append(block)

    def validate(self):
        for i in range(len(self.blocks)):
            assert i == 0 or self.blocks[i].prev_hash == self.blocks[i - 1].hash()
            self.blocks[i].validate()