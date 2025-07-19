#!/bin/bash
#SBATCH -p mesonet 
#SBATCH --account=m25031
#SBATCH --job-name=pddbind
#SBATCH -N 1
#SBATCH -c 6
#SBATCH --gpus=1
#SBATCH --time=10:00:00
#SBATCH --mem=120G


python scripts.py