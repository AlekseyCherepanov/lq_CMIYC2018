# -*- coding: utf-8 -*-
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to prepare /home/results/

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - see TODO and %%
# - resulting john.pot and mixed.potpw are incomplete
# - mixed.potpw should be disabled and removed when it turned out to
#   be useless
# - hardcoded paths
# - hardcoded list of hash formats; hardcoded fixes
# - submitted/ should be public
# - it does not handle HEX and/or hashcat's .pot format
# - it may interfere with scp of /home/results giving inconsisting
#   state (or may not?)

# Usage: just run in any private folder without arguments.
# It needs hashes in canonical form under
# /home/results/hashes-canon/
# For mixed.potpw, it needs original file at
# /home/share/hashes/pro_hashes/pro_hashes.txt
# It fills
# /home/results/cracked/*.txt
# /home/results/uncracked/*.pw
# /home/results/john.pot
# /home/results/mixed.potpw

import glob
import os

hh_submitted = {}

for fname in glob.glob('/home/worker/new/submitted/*'):
    with open(fname, 'rb') as f:
        for l in f:
            l = l.strip('\r\n')
            # we ignore partial lines silently
            # %% keep log of known and show new
            # %% : may be a part of password, check hash for correctness
            if ':' not in l:
                continue
            h, p = l.split(':', 1)
            if len(h) == 32:
                h = '$dynamic_0$' + h
            hh_submitted[h] = p

os.system('rm -rf generated/')
os.system('mkdir -p generated/cracked ; mkdir generated/uncracked')

formats = 'raw-md5 salted-sha1 md5crypt bcrypt'.split(' ')

with open('generated/john.pot', 'wb') as pf:
    for fo in formats:
        with open('/home/results/hashes-canon/' + fo + '.pw', 'rb') as f:
            with open('generated/cracked/' + fo + '.txt', 'wb') as cf:
                with open('generated/uncracked/' + fo + '.pw', 'wb') as uf:
                    for l in f:
                        l = l.rstrip('\n')
                        if l in hh_submitted:
                            p = hh_submitted[l]
                            p += '\n'
                            cf.write(p)
                            pf.write(h + ':' + p)
                        else:
                            uf.write(l + '\n')

with open('generated/mixed.potpw', 'wb') as mf:
    with open('/home/share/hashes/pro_hashes/pro_hashes.txt', 'rb') as f:
        for l in f:
            l = l.rstrip('\n')
            if len(l) == 32:
                l = '$dynamic_0$' + l
            if l in hh_submitted:
                # hash : password
                # otherwise just hash
                l = l + ':' + hh_submitted[l]
            mf.write(l + '\n')

os.system('mv generated/cracked/* /home/results/cracked/')
os.system('mv generated/uncracked/* /home/results/uncracked/')
os.system('mv generated/john.pot generated/mixed.potpw /home/results/')
