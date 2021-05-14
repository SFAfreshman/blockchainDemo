# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:22:21 2021

@author: Lenovo
"""
from blockchain import Blockchain
God = '00000000-0000-0000-0000-000000000000'
class Ledger(Blockchain):
    #查账户余额:入参:账本
    def balance(self,uid):
        #初始化余额为0
        balance=0
        for block in self.blocks:
            for item in block.items:
                if item.receiver==uid:
                    balance=balance+item.amount
                if item.sender==uid:
                    balance=balance-item.amount
        return balance
    def add(self, block):
        for transaction in block.items:
            if self.balance(transaction.sender) < transaction.amount and transaction.sender != God:
                 print("转账失败，账户余额不足,余额为{},支出为{}".format(self.balance(transaction.sender),transaction.amount))
            ##不满足条件则抛出异常
            assert transaction.sender == God or self.balance(transaction.sender) >= transaction.amount
        #重写方法治好调用方法    
        super().add(block)
                    
        
        
    