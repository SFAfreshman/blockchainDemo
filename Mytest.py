# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:57:49 2021

@author: Lenovo
"""

#建立一个区块链,从上帝开始发钱给用户
import json
import random
from uuid import uuid4
from blockchain import Blockchain, Block
from transaction import Transaction
from ledger import Ledger
God = '00000000-0000-0000-0000-000000000000'
if __name__ == '__main__':
    angels=[]#二级用户：天使
    ledger = Ledger()
    for i in range(3):
        block = Block()
        transaction = Transaction(sender=God, receiver=str(uuid4()),
                                      amount=random.randint(100, 10000))
        block.add(transaction)
        angels.append(transaction.receiver)
        ledger.add(block)
    for angel in angels:
        #由上帝下级天使继续发钱
        block = Block()
        transaction = Transaction(sender=angel, receiver=str(uuid4()),
                                      amount=random.randint(100, 10000))
        block.add(transaction)
        ledger.add(block)
        
    print(json.dumps(json.loads(str(ledger)), indent=4, sort_keys=True))
    print(ledger.validate())
