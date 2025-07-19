#!/bin/bash

#SBATCH -p mesonet
#SBATCH --account=m25031
#SBATCH --time=02:00:00
#SBATCH -N 1
#SBATCH -c 32
#SBATCH --gpus=1
#SBATCH --mem=128G

if [ $# -lt 2 ]; then
    echo "Please pass at least two arguments [MODEL_NAME DATASETS]"
    exit 1
fi

python test.py $@
