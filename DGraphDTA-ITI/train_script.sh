#!/bin/bash

#SBATCH -p mesonet
#SBATCH --account=m25031
#SBATCH --time=06:00:00
#SBATCH -N 1
#SBATCH -c 32
#SBATCH --gpus=1
#SBATCH --mem=256G

if [ $# -lt 2 ]; then
    echo "Please pass at least two arguments.8 [MODEL_NAME DATASETS]"
    exit 1
fi

python training.py $@
