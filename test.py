# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:47:11 2021

@author: Lenovo
"""

import json
import random
from uuid import uuid4
from blockchain import Blockchain, Block
from transaction import Transaction
if __name__ == '__main__':
    chain = Blockchain()
    for i in range(3):
        block = Block()
        for j in range(10):
            transaction = Transaction(sender=str(uuid4()), receiver=str(uuid4()),
                                      amount=random.randint(1, 1000000)
                                      )
            block.add(transaction)
        chain.add(block)
#if __name__ == '__main__':
#    print(json.dumps(json.loads(str(chain)), indent=4, sort_keys=True))
#    print(chain.validate())
#测试更改        
if __name__ == '__main__':
    chain.blocks[0].items[0].receiver = str(uuid4())
    print(json.dumps(json.loads(str(chain)), indent=4, sort_keys=True))
    print(chain.validate())
#    