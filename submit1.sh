#!/bin/bash
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to do submissions after simple.py or similar script; CMIYC 2018 edition

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - submitted/ should be public

if [ -s to_submit.txt ]; then
    mkdir -p submitted/
    file="submitted/`date -Iseconds`.txt"
    mv to_submit.txt "$file"
    ln -sf "$file" sent.txt

    gpg --trust-model always -a -o email.tmp -r sub-2018@contest.korelogic.com -se sent.txt
    mutt -s "cracked" sub-2018@contest.korelogic.com < email.tmp
    rm email.tmp
else
    echo submit1.sh: Empty to_submit.txt, skipped.
fi
