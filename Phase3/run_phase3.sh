#!/bin/sh

for file in Phase2/output/$1/*
do
echo $file
	python Phase3/Phase3.py $file Phase3/output/$1 /$(basename $file)
done
