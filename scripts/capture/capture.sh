#!/usr/bin/env bash

argc=4
if [[ $# -ne $argc ]]; then
    echo "Illegal number of parameters. Must be $argc."
    exit 1
fi
re='^[0-9]+$'
if ! [[ $1 =~ $re ]] ; then
    echo "error: $1 is not a number" >&2
    exit 1
fi
if ! [[ $2 =~ $re ]] ; then
    echo "error: $2 is not a number" >&2
    exit 1
fi
if ! [[ $3 != cm || $3 != mm || $3 != um ]] ; then
    echo "error: $3 must be cm, mm or um" >&2
    exit 1
fi

mkdir -p captures
stty -F /dev/serial0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
exec 3<> /dev/serial0

for (( i=0; i<$(($1)); i++ ))
do
    # Prend une capture d'image
    path="captures/$4$i.jpg"
    fswebcam -q -p GREY "$path%S" -F 5 -R
    echo $path

    #Deplace la plateforme
    echo "m$2$3" >&3
    echo "m$2$3"

    #Attend la fin du mouvement
    while read -ru 3 output
    do
        echo $output
        if [[ $output == *"DONE"* ]]; then
            break
        elif [[ $output == *"FRONT_SWITCH"* || $output == *"BACK_SWITCH"* || $output == *"SOFT_STOP"* ]]; then
            echo "Arret imprevu:"
           break
        fi
    done
done
