# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to prepare submissions as simple as possible; CMIYC 2018 edition

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - see TODO and %%
# - it does not handle HEX and/or hashcat's .pot format
# - submitted/ should be public
# - it sends everything as is, so orgs do the hard work

import glob

hh = {}

for fname in glob.glob('/home/received/*'):
    # %% it could be just /[0-9]* above.
    if fname.rsplit('/', 1)[-1].rstrip('0123456789') == '':
        with open(fname, 'rb') as f:
            for l in f:
                if l.startswith("h "):
                    l = l.rstrip('\n')
                    letter, time, h = l.split(' ', 2)
                    hh[h] = 1

for fname in glob.glob('/home/share/*.pot'):
    with open(fname, 'rb') as f:
        for l in f:
            l = l.strip('\n')
            hh[l] = 1

hh_submitted = {}

for fname in glob.glob('/home/worker/new/submitted/*'):
    with open(fname, 'rb') as f:
        for l in f:
            l = l.strip('\n')
            hh_submitted[l] = 1

to_submit = []

for h in hh.iterkeys():
    h = h.rstrip('\r')
    if h.startswith("$dynamic_0$"):
        h = h[len("$dynamic_0$") : ]
    if h not in hh_submitted:
        to_submit.append(h)

with open('to_submit.txt', 'w') as f:
    for h in to_submit:
        f.write(h + '\n')
