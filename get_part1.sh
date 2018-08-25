#! /bin/sh
# WARNING: LOW QUALITY; it is a dirty prototype, not a good software.

# grep-like utility to pick hashes for client_run.sh

# Copyright © 2018 Aleksey Cherepanov <lyosha@openwall.com>
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

# TODO: Known problems:
# - hardcoded paths
# - races were not investigated
# - it may overwrite a file (very unprobable case)
# - see TODO

SIZE="$1"

FNAME="bp1-$USER-`mktemp XXXXXXXX`.pw"

perl -e '

use List::Util qw/shuffle/;

open(IN, "<", "/home/results/uncracked/bcrypt.pw");
@a = <IN>;
close(IN);
chomp(@a);

%h = ();
for (</home/share/bcrypt_parts1/*.pw>) {
    open(T, "<", $_);
    @b = <T>;
    close(T);
    chomp(@b);
    for (@b) {
        $h{$_} = 1;
    }
}

@a = grep { !$h{$_} } @a;
@a = shuffle(@a);

for (@a[0 .. $ARGV[0] - 1]) {
    # TODO: it produces empty lines in the end of work.
    print "$_\n";
}

' "$SIZE" > "/home/share/bcrypt_parts1/$FNAME"

echo "$FNAME"
