#!/usr/bin/env bash
source venv/bin/activate

method=$1
threshold_method=$2
images_dir=$3
parentname="$(basename "$images_dir")"
output_file="${parentname}_${method}_${threshold_method}.csv"

for image in $images_dir/*;
do
	#Keep only the file name
	filename=$(basename $image)
	#Remove the extension
	filename=${filename%.*}
	filename=${filename##*/}
	#Parse file name to get the distance and the capture index
	IFS='-' read distance index <<< "$filename"

	line="${distance};${index};"
	line+=$(python center-finder.py $image $method -t $threshold_method)
	echo "${line} >> ${output_file}"
	echo $line >> $output_file
done

deactivate
