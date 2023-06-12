#!/bin/bash
# --- Hera
#SBATCH -J gross4
#SBATCH -e gross4.err
#SBATCH -o gross4.out
#SBATCH -t 5:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov
# --- Hera


#--- WCOSS2
##PBS -N rtofs_eval
##PBS -o rtofs_eval
##PBS -j oe
##PBS -A ICE-DEV
##PBS -q hera
##PBS -l walltime=1:00:00
##PBS -l select=1:ncpus=1
#--- WCOSS2


#. $HOME/rgdev/toolbox/misc/python_load.wcoss2
. $HOME/rgdev/toolbox/misc/python_load.hera


#------------------------ General across platforms --------------
export MODEL=rtofs_cice
export modelout=$HOME/clim_data/rtofs_gross

export GDIR=$HOME/rgdev/ice_scoring/gross_checks/

export PYTHONPATH=$PYTHONPATH:$GDIR/shared

if [ ! -d $HOME/scratch/gross/$MODEL ] ; then
  mkdir -p  $HOME/scratch/gross/$MODEL
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$MODEL
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$MODEL

ln -sf $GDIR/curves curves
time $GDIR/$MODEL/${MODEL}_scan.sh


#after check has been done -- summaries and graphics
# beta.$tag.${lead}
cat beta.*.* > all
for lead in n00 f24 f48 f72 f96 f120 f144 f168 f192
do
  cat beta.*.$lead > all.$lead
done


# For plots, last number is dot size. Expect fewer pts as go down list, 
#    so make pts larger
python3 $GDIR/graphics/plot_errs.py all all 1.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions all > nonphysical
python3 $GDIR/graphics/plot_errs.py nonphysical nonphysical 2.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical > unknown
python3 $GDIR/graphics/plot_errs.py unknown unknown 4.

$GDIR/$MODEL/split.sh unknown | sort -n
