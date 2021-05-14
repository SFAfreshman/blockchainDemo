# -*- coding: utf-8 -*-
"""
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
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    def on_message(self, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            logging.warning('Cannot parse request message: %s', message)
            self.write_message(json.dumps({
                'status': 500,
                'error': 'Cannot parse request message.',
                'response': None
            }))
        else:
            if message is not None:
                if 'op' in message:
                    if message['op'] == 'register':
                        if 'args' in message and 'addr' in message['args']:
                            peers = pickle.loads(db.get('peers'))
                            if not isinstance(message['args']['addr'], list):
                                message['args']['addr'] = [str(message['args']['addr'])]
                            for addr in message['args']['addr']:
                                if addr.startswith('ws://') or addr.startswith('wss://'):
                                    peers.add(addr)
                            db.set('peers', pickle.dumps(peers))
                            self.write_message(json.dumps({
                                'status': 202,
                                'success': 'Accepted'
                            }))
                        else:
                            self.write_message(json.dumps({
                                'status': 500,
                                'error': 'Operation "register" requires the following "args": "addr"',
                                'response': None
                            }))
                    elif message['op'] == 'peers':
                        self.write_message(json.dumps({
                            'status': 200,
                            'success': 'Ok',
                            'response': {'peers': list(pickle.loads(db.get('peers')))}
                        }))
                    elif message['op'] == 'time':
                        self.write_message(json.dumps({
                            'status': 200,
                            'success': 'Ok',
                            'response': {
                                'time': datetime.now().timestamp(),
                                'time_zone': datetime.now(timezone.utc).astimezone().tzname()
                            }
                        }))
                    else:
                        self.write_message(json.dumps({
                            'status': 404,
                            'error': 'Operation "{}" is not supported'.format(message['op']),
                            'response': None
                        }))
                else:
                    logging.warning('Message body is not supported: %s', message)
                    self.write_message(json.dumps({
                        'status': 500,
                        'error': 'Message body is not supported.',
                        'response': None
                    }))

    def check_origin(self, origin: str):
        return True

    def open(self):
        logging.info('Client connected: %s', self.request.remote_ip)
        if self not in clients:
            clients.append(self)

    def on_close(self):
        if self in clients:
            clients.remove(self)

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
    # pickle:将Python 的对象序列化与反序列化,并配置日志
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    db = Redis(args.redis)
    if b'peers' not in db.keys():
        db.set('peers', pickle.dumps(set([])))
    #WebSocket
    web.Application([
            (r'/', IndexHandler),
            (r'/ws', SocketHandler)
    ]).listen(args.port)
    logging.info('Tornado is listening on port: %d', args.port)
    ioloop.IOLoop.instance().start()