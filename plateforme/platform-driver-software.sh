#!/usr/bin/env bash

stty -F /dev/serial0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

( cat < /dev/serial0 ) &

while true
do
	read input
	echo "$input\n" > /dev/serial0
done
