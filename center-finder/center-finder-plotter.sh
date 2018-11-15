#!/usr/bin/env bash
source venv/bin/activate

for filename in $1/*
do
	line="$filename,"
	line+=$(python center-finder.py "$filename" centroid -threshold_method log)
	echo $line
	echo $line >> center-finder-plotter-output.csv
done


deactivate
