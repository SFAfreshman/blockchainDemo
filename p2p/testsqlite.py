# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 22:06:02 2021

@author: Lenovo
"""

import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")
c = conn.cursor()
c
c.execute("INSERT INTO student(id,name,sex,classname) VALUES(NULL,'Zhang',0,'gg51')")
print ("Insert successfully")
conn.commit()
conn.close()
#INSERT INTO student VALUES(NULL,'Wang',0,'gg51'); 
#INSERT INTO student VALUES(NULL,'Zhao',1,'gg52'); 
#INSERT INTO student VALUES(NULL,'Li',0,'gg52'); 
#INSERT INTO student VALUES(NULL,'Fang',1,'gg51')
#