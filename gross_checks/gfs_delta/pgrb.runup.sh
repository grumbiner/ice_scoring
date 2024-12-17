#!/bin/sh
#

source $HOME/env3.10/bin/activate
export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/gross_checks/shared/

#for cyc in 00 06 12 18
#do
cyc=00

#for dd in 19 20 21 22 23
for dd in 20 21 22 23
do
  export tag=202402$dd

  ctrla=$HOME/noscrub/conctest/ctrl${cyc}/gfs.${tag}/${cyc}/atmos
  expta=$HOME/noscrub/conctest/test${cyc}/gfs.${tag}/${cyc}/atmos

  ctrlb=$HOME/noscrub/conctest/pgrb/ctrl${cyc}/gfs.${tag}/${cyc}/atmos
  exptb=$HOME/noscrub/conctest/pgrb/test${cyc}/gfs.${tag}/${cyc}/atmos

  if [ ! -d ${tag}$cyc ] ; then
    mkdir ${tag}$cyc
  fi

  # Loop over all leads:
  #set -x
  export hhh=000
  delta=1
  while [ $hhh -le 384 ]
  #while [ $hhh -le 24 ]
  do
    #A:
    fna=gfs.t${cyc}z.pgrb2.0p25.f${hhh}
    #B:
    fnb=gfs.t${cyc}z.pgrb2b.0p25.f${hhh}
  
    python3 grib_bootstrap.py $ctrla/$fna $expta/$fna > a.${hhh}.$tag 
    python3 grib_bootstrap.py $ctrlb/$fnb $exptb/$fnb > b.${hhh}.$tag 
  
    mv [ab].${hhh}.$tag ${tag}$cyc
  
    if [ $hhh -ge 120 ] ; then
      delta=3
    fi
    hhh=`expr $hhh + $delta`
  
    if [ $hhh -lt 10 ] ; then
      hhh=00$hhh
    elif [ $hhh -lt 100 ] ; then
      hhh=0$hhh
    fi

  done

done
