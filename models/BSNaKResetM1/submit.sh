#!/bin/bash 

#$ -S /bin/bash
#$ -q fulla.q
#$ -cwd
#$ -o log/$JOB_NAME.$JOB_ID.log
#$ -e log/$JOB_NAME.$JOB_ID.err

python $1 ${@:2}
