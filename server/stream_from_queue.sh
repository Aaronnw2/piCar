#!/bin/bash

die () {
    echo >&2 "Must pass mode (-m or --mode of display, train, or track)"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"
echo $1 | grep -E -q 'display|track|train' || die
if [ -p buffer ]
    then
        rm buffer
fi
mkfifo buffer
python3 opencv_receive.py --mode $1 &
nc -l -p 2222 -v > buffer
