#!/usr/bin/env bash

stty -F /dev/serial0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

exec 1< /dev/serial0

while true
do
    read input
    echo $input > /dev/serial0
done
