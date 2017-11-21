#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    echo "Specify the serial port."
    exit 1
fi

stty -F $1 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

( cat $1 ) &

while true
do
    read input
    echo $input > $1
done
