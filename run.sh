#!/bin/bash
# Basic while loop
counter=1

while [ $counter -le 10 ]
do
	python blocksworld.py $1 $2
	#echo $counter
	((counter++))
done
echo All done