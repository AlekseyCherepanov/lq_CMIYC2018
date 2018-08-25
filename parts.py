# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to extract popular parts of passwords as in beginning+end

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - hardcoded paths
# - hardcoded level for popularity to be printed

import glob

hlist = []
# read cracks
for fname in glob.glob('results/cracked/*'):
    with open(fname) as f:
        for l in f:
            l = l.rstrip('\n')
            hlist.append(l)

hlist.sort()

lh = {}
rh = {}
uh = {}

for c in hlist:
    for i in range(2, len(c) - 2):
        l = c[ : i]
        r = c[i : ]
        if l not in lh:
            lh[l] = 0
        lh[l] += 1
        if r not in rh:
            rh[r] = 0
        rh[r] += 1
        if r not in uh:
            uh[r] = 0
        uh[r] += 1
        if l not in uh:
            uh[l] = 0
        uh[l] += 1

for k in lh.keys():
    lh[k] **= len(k)
for k in rh.keys():
    rh[k] **= len(k)
for k in uh.keys():
    uh[k] **= len(k)

oparts = {}

for c in hlist:
    # print
    b = 0
    bl, br = '', ''
    for i in range(2, len(c) - 2):
        l = c[ : i]
        r = c[i : ]
        # k = uh[l] * len(l) + uh[r] * len(r)
        k = uh[l] + uh[r]
        if k > b:
            b = k
            bl = l
            br = r
        # print '{}  |  {}   <- {}, {}'.format(
        #     l, r, lh[l], rh[r])
    if b != 0:
        # print '{}  |  {}   <- {}, {};   {}, {}'.format(
        #     bl, br, lh[bl], rh[br], uh[bl], uh[br])
        oparts[bl] = uh[bl]
        oparts[br] = uh[br]
    # else:
    #     print c

o = [ (v, k) for k, v in oparts.iteritems() ]
o.sort()

# print o[0 : 10]
# exit()

for k, v in reversed(o):
    if k < 20:
        break
    print v
