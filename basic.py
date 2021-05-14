# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:40:10 2021

@author: Lenovo
"""

import hashlib
from wrenchbox.object import Dict2StrSafe
class Base(Dict2StrSafe):
    def hash(self):
        return hashlib.sha1(str(self.__dict__).encode()).hexdigest()