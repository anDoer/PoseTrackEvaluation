#!/bin/bash

echo $1
echo $2
echo $3
echo $4
echo $5

#source $1

cd $2 && export PYTHONPATH=$PWD/../py-motmetrics:$PYTHONPATH

GroundTruthDir=$3
PredictionDir=$4

	python evaluate.py \
	  --groundTruth=$GroundTruthDir \
	  --predictions=$PredictionDir \
	  --$5
