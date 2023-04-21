#!/bin/bash
#SBATCH --time=600
#SBATCH --mem=50gb
#SBATCH -p sched_mit_darwin

python collate_cocco_data.py 50 75
