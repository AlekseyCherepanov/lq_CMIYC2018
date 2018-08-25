# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to find popular substrings in cracks

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

import glob
import sys

hlist = []
# read cracks
for fname in [ sys.argv[1] ]:
    with open(fname) as f:
        for l in f:
            l = l.rstrip('\n')
            hlist.append(l)

h = {}

# for c in hlist:
#     for l in range(3, len(c) - 2):
#         for i in range(0, len(c) - l):
#             part = c[i : i + l]
#             assert len(part) == l
#             if part not in h:
#                 h[part] = 0
#             h[part] += 1

for c in hlist:
    for l in range(3, len(c)):
        part = c[0 : l]
        if part not in h:
            h[part] = 0
        h[part] += 1
        # part = c[-l : ]
        # if part not in h:
        #     h[part] = 0
        # h[part] += 1

o = [ (v, k) for k, v in h.iteritems() ]
o.sort()

for v, k in o:
    print v, k
