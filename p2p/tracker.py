# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 15:50:06 2021

@author: Lenovo
"""

import argparse
import json
import logging
import threading
import time
import traceback
#from tornado import websocket
#from app import websocket 
import websocket
from wrenchbox.logging import setup_log
DEFAULTS = {'max_connection': 3}

    #为啥报错说没有Tracker() 单个py文件和py project有啥区别
    #如何启动测试
class Tracker:
    def __init__(self):
        self.spawning = []
        self.peers = []
    def run(self, seed: str, sleep: int = 30):
        self.spawn(seed)
        while True:
            time.sleep(sleep)
            self.query()
            self.announce()
            if not len(self.peers):
                logging.critical('All peers are gone, updater will terminate.')
                break
    def spawn(self, url):
        if url not in self.spawning:
            self.spawning.append(url)
            logging.info('Spawning new peer: %s', url)
            ws = websocket.WebSocketApp(
                    url=url,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_close=self.on_close
                    )
            peer = threading.Thread(target=ws.run_forever)
            peer.daemon = True
            peer.start()
            self.spawning.remove(url)
    #WebSocket相关的事件监听函数
    def on_open(self, ws):
        logging.info("New peer connected: %s", ws.url)
        self.peers.append(ws)
    def on_close(self, ws):
        logging.info("Peer disconnected: %s", ws.url)
        if ws in self.peers:
            self.peers.remove(ws)
    def on_message(self, ws, message):
        if len(self.peers) >= DEFAULTS['max_connection']:
            return
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            pass
        if 'response' in message and 'peers' in message['response']:
            for peer in message['response']['peers']:
                if peer not in [i.url for i in self.peers]:
                    self.spawn(peer)
    def query(self):
        for peer in self.peers:
            try:
                peer.send(json.dumps({
                        'op': 'peers'
                        }))
            except:
                logging.error('Cannot request peers from: %s', peer.url)
                traceback.print_exc()
    def announce(self):
        for peer in self.peers:
            try:
                peer.send(json.dumps({
                        'op': 'register',
                        'args': {
                                'addr': [i.url for i in self.peers]
                                }
                        }))
            except:
                pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        action='store_true'
                        , default=False, help='show debug information')
    parser.add_argument('-t', 
                        '--sleep',
                        type=int, default=30, help='refresh rate in seconds, default: 30')
    parser.add_argument('seed',
                        type=str, help='seed announce server, e.g.: ws://localhost:9000/ws')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    Tracker().run(args.seed, args.sleep)