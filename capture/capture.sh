#!/usr/bin/env bash

argc=5
if [[ $# -ne $argc ]]; then
    echo "Illegal number of parameters. Must be $argc."
    exit 1
fi
re='^[0-9]+$'
if ! [[ $2 =~ $re ]] ; then
    echo "error: $2 is not a positive number" >&2
    exit 1
fi
re='\-?[0-9]+'
if ! [[ $3 =~ $re ]] ; then
    echo "error: $3 is not a number" >&2
    exit 1
fi
if ! [[ $4 != cm || $4 != mm || $4 != um ]] ; then
    echo "error: $4 must be cm, mm or um" >&2
    exit 1
fi

mkdir -p captures
stty -F /$1 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
exec 3<> $1

for (( i=0; i<$(($2)); i++ ))
do
    # Prend une capture d'image (TODO : meilleure convention de nommage, les fichiers sont dur a trier)
    path="captures/$5$i.jpg"
    fswebcam -q -r 1280x960 --no-banner "$path"
    echo $path

    #Deplace la plateforme
    echo "m$3$4" >&3
    echo "m$3$4"

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
