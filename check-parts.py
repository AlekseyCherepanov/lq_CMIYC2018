# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to check a list of parts against cracks to find combinations

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# Usage:
# python check-parts.py file_with_parts
# - results/cracked/* should be lists with cracked passwords;
# - it creates file_with_parts.check_found with the found passwords.
# Prints:
# - parts with number of uses (1 part used twice in 1 passwords gives +2)
# - number of passwords and stats by length
# - possible parts based on remaining tails with stats

# TODO: Known problems:
# - hardcoded paths
# - see TODO and %%
# - creates files silently
# - UI could be improved

import sys
import glob
from pprint import pprint

mp_list = []
with open(sys.argv[1]) as f:
    for l in f:
        l = l.rstrip('\n')
        mp_list.append(l)

mp = set(mp_list)

hlist = []
# read cracks
for fname in glob.glob('results/cracked/*'):
    with open(fname) as f:
        for l in f:
            l = l.rstrip('\r\n')
            hlist.append(l)

hp = {}

def check(tail, top = False):
    if tail in mp:
        # tail is a part itself
        return [ tail ]
    for l in range(len(tail), 0, -1):
        p = tail[ : l]
        if p not in mp:
            continue
        # p is a known part, check tail
        r = check(tail[l : ])
        if r:
            return [ p ] + r
        # tail does not match, try next part; in case of shorter part
    if not top:
        if tail not in hp:
            # if tail == '2018!!':
            #     print '>>>>> bad bad ', mp
            hp[tail] = 0
        print 'hp:', c, '|', tail
        hp[tail] += 1
    # no parts matched
    return False

h = {}

of = open(sys.argv[1] + '.check_found', 'w')

kk = 0
lh = {}
for c in hlist:
    r = check(c, top = c)
    if r:
        kk += 1
        of.write(''.join(r) + '\n')
        l = len(r)
        if l not in lh:
            lh[l] = 0
        lh[l] += 1
        if l == 5:
            print r
        # if l == 6:
        #     print r
        # if '020171' in r:
        #     print r
        for p in r:
            if p not in h:
                h[p] = 0
            h[p] += 1
# pprint(h)

o = [ (v, k) for k, v in h.iteritems() ]
o.sort()
for v, k in reversed(o):
    print v, k

print

print kk
pprint(lh)

print

o = [ (v, k) for k, v in hp.iteritems() ]
o.sort()
o = o[-200 : ]
for v, k in o:
    print v, k
