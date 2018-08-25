#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to track .pot file and upload cracks to the server ASAP

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - see TODO and %%
# - unfriendly UI
# - it may send partial lines
# - it may loose lines on reconnection
# - delay for reconnection may grow big
# - python 2 only
# - windows was not tested
# - chosen port does not in some networks; port forwarding with
#   127.0.0.1 will do the trick, but may break certificate checking

import sys
import ssl
import socket
import os.path
import time
import traceback

assert sys.version_info[0] == 2, 'It requires python 2. Try python2 command.'

SERVER = 'the.server.com'
# SERVER = '127.0.0.1'
PORT = 20000
SECRET = 'THE_SECRET_AS_IN_pot_receiver.py'

assert len(sys.argv) == 4, 'Usage: python pot_sender.py <user> <machine> <path/to/john.pot>'

# %% check for spaces too
user = sys.argv[1]
assert '\n' not in user, 'specify differently'
machine = sys.argv[2]
assert '\n' not in machine, 'specify differently'

pot = sys.argv[3]
assert pot.endswith(".pot"), 'path to john.pot should end with ".pot"'

if not os.path.exists(pot):
    os.umask(0077)
    with open(pot, 'a') as f:
        pass

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, PORT))
    # %% we don't check certificate, it is bad
    ss = ssl.wrap_socket(s)
    ss.send(SECRET + ' ' + user + ' ' + machine + '\n')
    t = ss.recv(10)
    if t != 'OK SECRET\n':
        print t
    t = ss.recv(8)
    if t != 'OK USER\n':
        print t
    return ss

# sock = None
sock = connect()

delay = 0

with open(pot, 'rb') as f:
    while True:
        l = f.readline()
        if l == '':
            # %% do it like tail -f
            time.sleep(2)
        else:
            # print l
            try:
                if sock == None:
                    sock = connect()
                    delay = 0
                sock.send(l)
            except:
                if sock != None:
                    sock.close()
                    sock = None
                t = traceback.format_exc()
                print t
                time.sleep(delay)
                delay += 10
                print 'Due to error, delay after next error will be', delay
