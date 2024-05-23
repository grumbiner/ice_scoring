#!/bin/sh
#SBATCH -J yrexpt
#SBATCH -e slurm%j.err
#SBATCH -o slurm%j.out
#SBATCH --partition=batch
#SBATCH --account=nggps_emc
#SBATCH --clusters=c5
#SBATCH --time=4:59:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

cd $HOME/rgdev/ice_scoring/NCEP_si_verf/
source ~/env3.9/bin/activate
# args are CICE testid, number of experiments, and concentration cutoff
time python3 year_cice.py gen5 96 0.15
