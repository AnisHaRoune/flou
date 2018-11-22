#!/usr/bin/env bash
source venv/bin/activate

method=$1
threshold_method=$2
images_dir=$3
output_file="center-finder_${method}_${threshold_method}.csv"

i=0
for image in $images_dir/*;
do
	line="${i},${image},"
	line+=$(python center-finder.py $image $method -t $threshold_method)
	echo "${line} >> ${output_file}"
	echo $line >> $output_file
	i=$((i+1))
done

deactivate
