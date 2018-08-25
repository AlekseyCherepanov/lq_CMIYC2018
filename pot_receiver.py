# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to receive cracks from .pot files tracked by pot_sender.py
# It should be started in /home/received/

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - hardcoded paths
# - see TODO and %%
# - it starts well without key.pem and cert.pem, but fails on the
#   first connection; inconvenient

import ssl
import socket
import os.path
import traceback
import time
import contextlib
from threading import Thread

SECRET = 'CHANGE_THIS'
PORT = 20000

SERVER = '0.0.0.0'

INDEX_FILE = 'pot_receiver.index'

# approximate max size of file for log per connection
MAX_SIZE = 100 * 1000 * 1000

class handler(object):
    def __init__(self, socket, addr, index):
        self.socket = socket
        self.addr = addr
        self.index = str(index)
        self.size = 0
        self.f = None
        self.run()
    def put(self, letter, s):
        s = s.rstrip('\n')
        # %% we might save time of start and subtract it to save space
        n = letter + ' ' + str(time.time()) + ' ' + s + '\n'
        self.f.write(n)
        self.f.flush()
        self.size += len(n)
    def run(self):
        with open(self.index, 'w') as f:
            self.f = f
            try:
                self.put('i', repr(self.addr))
                ss = ssl.wrap_socket(self.socket,
                                     server_side = True,
                                     keyfile = 'key.pem',
                                     certfile = 'cert.pem')
                secret = ss.read(len(SECRET) + 1)
                if SECRET + ' ' != secret:
                    self.put('W', secret)
                    ss.send('BAD SECRET\n')
                else:
                    ss.send('OK SECRET\n')
                    with contextlib.closing(ss.makefile()) as ssf:
                        l = ssf.readline()
                        l = l.strip()
                        # %% check user to be valid, find space
                        self.put('u', l)
                        ss.send('OK USER\n')
                        while True:
                            l = ssf.readline()
                            if l == '':
                                self.put('E', 'eof')
                                break
                            l = l.rstrip('\n')
                            self.put('h', l)
                            # if self.size >= MAX_SIZE:
                            #     self.put('C', 'size')
                            #     break
                            # %% sender can't know how many hashes we got
            except:
                t = traceback.format_exc()
                print 'Connection:', self.index
                print t
                self.put('e', repr(t))
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

def the_server():
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w') as f:
            f.write('0')
    with open(INDEX_FILE, 'r') as f:
        index = int(f.read())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER, PORT))
    s.listen(1)
    while True:
        # %% anti-ddos, one can eat all connections
        conn, addr = s.accept()
        index += 1
        with open(INDEX_FILE, 'w') as f:
            f.write(str(index))
        t = Thread(target = handler, args = (conn, addr, index))
        t.start()

if __name__ == '__main__':
    the_server()
