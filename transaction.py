# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:41:12 2021

@author: Lenovo
"""

from datetime import datetime
from uuid import UUID
from basic import Base
class Transaction(Base):
    def __init__(self,sender: str, receiver: str,amount: int,t: float = None,prev_hash: str = None):
        assert UUID(sender, version=4)
        assert UUID(receiver, version=4)
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.t = t if t is not None else datetime.now().timestamp()
        self.prev_hash = prev_hash