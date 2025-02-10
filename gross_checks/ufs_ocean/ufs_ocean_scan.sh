#!/bin/sh 

#Hera:
echo zzz HOME = $HOME
export PYTHONPATH=/home/Robert.Grumbine/rgdev/mmablib/py:/home/Robert.Grumbine/rgdev/ice_scoring/gross_checks/shared
export MODDEF=/home/Robert.Grumbine/rgdev/ice_scoring/model_definitions

echo zzz module list
module list

set -x

export level=moderate

for f in 20191203 20191206 20191209 20191212 20191215 20191218 20191221 20191224 20191227 20191230 20200102 20200105 20200108 20200111 20200114 20200117 20200120 20200123 20200126 20200129 20200201 20200204 20200207 20200210 20200213 20200216 20200219 20200222 20200225 20200601 20200604 20200607 20200610 20200613 20200616 20200619 20200622 20200625 20200628 20200701 20200704 20200707 20200710 20200713 20200716 20200719 20200722 20200725 20200728 20200731 20200803 20200806 20200809 20200812 20200815 20200818 20200821 20200824 20200827 20200830
do
  tag=$f
  j=0
#  while [ $j -le 15 ]
#  do
  for fhr in 006 030 054 078 102 126 150 174 198 222 246 270 294 318 342 366
  do
      time python3 $GDIR/ufs_ocean/ufs_ocean.py \
             $modelout/gfs.$f/00/model/ocean/history/gfs.ocean.t00z.6hr_avg.f${fhr}.nc \
             $GDIR/ufs_ocean/ufs_ocean.$level redone \
             > ocean.${f}.$level.$fhr.results
  done

done

cat ocean.*.results > all
for lead in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
  fhr=`expr $lead \* 24 + 6`
  if [ $fhr -lt 10 ] ; then
    fhr=00$fhr
  elif [ $fhr -lt 100 ] ; then
    fhr=0$fhr
  fi

  #cat ocean.subset.*.lead${lead}.results > all.lead.$lead
  cat ocean.subset.*.$level.$fhr.results > all.fhr.$lead
done

