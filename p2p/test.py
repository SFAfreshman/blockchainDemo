# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 20:41:16 2021

@author: Lenovo
"""

import argparse
import json
import logging
import pickle
from redis import Redis
from tornado import websocket, web, ioloop
from wrenchbox.logging import setup_log
DEFAULTS = {'port': 9000}
clients = []
db = None
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
    '--debug',
    action='store_true'
    ,
    default=False, help='show debug information'
    )
    parser.add_argument(
    '-p', 
    '--port',
    type=int,
    default=DEFAULTS['port'],
    help='listening port, default: {}'.format(DEFAULTS['port'])
    )
    parser.add_argument(
    '-r', 
    '--redis'
    ,
    type=str,
    default='redis.db'
    ,
    help='redis database file, default: redis.db'
    )
    args, _ = parser.parse_known_args()
    print(args)