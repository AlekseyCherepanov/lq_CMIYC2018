#! /bin/sh
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# Script to distribute work on bcrypt hashes with hardcoded wordlist

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - hardcoded paths
# - it may cycle infinitely in the end of the work (filing up space)
# - it lefts a lot of files on every worker node
# - john does not respond to input for status, try bash -i either for the script or for john only
# - "SOMETHING FAILED" banner would not be showed if john receives a signal; could traps help?
# - taken parts of work are not returned automatically on failures/timeout
# - it trusts names of files given by the server

# ######################################################################

# Settings: make a copy of script and change values.

# --crack-status is set for john. We are not going to have a lot of
# and john in scipt does not react to input.
# Or use `killall -USR1 john`. Please don't forget -USR1

# Name of the contest server according to your ~/.ssh/config
SERVER=con

# Number of hashes to ask for.
# Please target 10-20 minutes. The wordlist is ~15k.
# So for 23 c/s per core ask 1-2 hashes * number of cores.
SIZE=24

# Your john, and remote worker

# To use this machine, use REMOTE="",
# otherwise it should be name from .ssh/config
REMOTE=""
# Don't use ~ ; enter full path
REMOTE_WORK_DIR="/home/user/"

# Don't use ~ ; enter full path
# or JOHN="john" if john is on PATH
JOHN="/home/user/JohnTheRipper/run/john"

# Number of cores to use
# You may add --device=1,2 for gpus
# Use FORK="" if you don't need fork
# FORK=""
FORK="--fork=12"
# FORK="--device=1,2 --fork=1"
# FORK="--device=1"

# Format name to use
# FORMAT=bcrypt-ztex
# FORMAT=bcrypt-opencl
FORMAT=bcrypt

# ######################################################################

while true; do

    FNAME="`ssh "$SERVER" /home/share/bdscripts/get_part1.sh "$SIZE"`" &&

        echo "In case of problem, please remove /home/share/bcrypt_parts1/$FNAME" &&

        scp "$SERVER":"/home/share/bcrypt_parts1/$FNAME" . &&

        ssh "$SERVER" 'grep -xvFf /home/results/cracked/bcrypt.txt /home/share/wordlists/pp_hashcat_hm.nocracks.15k_1' > pp_hashcat_hm.15k_1.remaining."$FNAME".txt &&

        if test "x$REMOTE" = "x"; then
            "$JOHN" --crack-status --session="$FNAME" --format="$FORMAT" "$FNAME" $FORK --wordlist=pp_hashcat_hm.15k_1.remaining."$FNAME".txt
        else
            scp "$FNAME" pp_hashcat_hm.15k_1.remaining."$FNAME".txt "$REMOTE":"$REMOTE_WORK_DIR" &&
                ssh "$REMOTE" "$JOHN" --crack-status --session="$REMOTE_WORK_DIR"/"$FNAME" --format="$FORMAT" "$REMOTE_WORK_DIR"/"$FNAME" $FORK --wordlist="$REMOTE_WORK_DIR"/pp_hashcat_hm.15k_1.remaining."$FNAME".txt
        fi || (

            echo
            printf '=%.0s' `seq 50`
            echo
            echo "SOMETHING FAILED"
            echo "Please remove $FNAME on the server"
            printf '=%.0s' `seq 50`
            echo
            echo
            false
        ) || exit 1

    # upload .pot here; or better use separate cycle, or pot_sender.py

done
