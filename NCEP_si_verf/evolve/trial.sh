#!/bin/sh
#SBATCH -J yrexpt
#SBATCH -e yrexpt%j.err
#SBATCH -o yrexpt%j.out
#SBATCH --partition=batch
#SBATCH --account=nggps_emc
#SBATCH --clusters=c5
#SBATCH --time=5:59:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

cd $HOME/rgdev/ice_scoring/NCEP_si_verf/evolve/
source ~/env3.9/bin/activate

# args are CICE testid, number of experiments, and concentration cutoff
time python3 year_cice.py gen9 90 0.15
