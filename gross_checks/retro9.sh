#!/bin/bash
#--- WCOSS2
#PBS -N ufs_ice_eval
#PBS -o ufs_ice_eval
#PBS -j oe
#PBS -A ICE-DEV
#PBS -l walltime=4:00:00
#PBS -l select=1:ncpus=1
#--- WCOSS2

# --- Hera
#SBATCH -J hr5
#SBATCH -e hr5.err
#SBATCH -o hr5.out
#SBATCH -t 5:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov
# --- Hera


set -x


# Hera:
#source /home/Robert.Grumbine/rg/env3.12c/bin/activate
# Wcoss2
source $HOME/env3.12/bin/activate

#export modelout=$HOME/clim_data/rtofs_gross
export modelout=$HOME/noscrub/retros/
export modeltag=ufs_ice
export MODEL=ufs_ice

#export GDIR=$HOME/rgdev/ice_scoring/gross_checks/
export GDIR=$HOME/noscrub/retros/gross_checks/


#------------------------ General across platforms --------------
set -x

export level=extreme

export PYTHONPATH=$PYTHONPATH:$GDIR/shared

if [ ! -d $HOME/scratch/gross/$modeltag ] ; then
  mkdir -p  $HOME/scratch/gross/$modeltag
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$modeltag
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$modeltag

ln -sf $GDIR/curves curves
time $GDIR/$MODEL/${MODEL}_scan.sh

# Now that all results have been scanned, check for errors:

# For plots, last number is dot size. Expect fewer pts as go down list, 
#    so make pts larger
for model in gfs gdas
do
  python3 $GDIR/graphics/plot_errs.py all.$model all.$model 12.

  python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions.$modeltag all.$model > nonphysical.$model
  python3 $GDIR/graphics/plot_errs.py nonphysical.$model nonphysical.$model 12.

  python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical.$model > unknown.$model
  python3 $GDIR/graphics/plot_errs.py unknown.$model unknown.$model 12.
done

for model in gfs gdas
do
  $GDIR/$MODEL/${MODEL}_split.sh unknown.$model | sort -n
  if [ ! -d $model ] ; then
    mkdir $model
  fi
  for f in *.s
  do
    python3 $GDIR/graphics/plot_errs.py $f $f 12
  done

  mv *.png *.s $model
  cd $model
  scp -p *.png rmg3@emc-lw-rgrumbi:website/retro/9/ufs_ice/$model
  cd ..

done

