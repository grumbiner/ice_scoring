#!/bin/sh

#Bootstrap for ice model verification -- 
#    retrieve the scripts and fixed files for a basic run of the system
#Robert Grumbine
# 25 February 2020

set -xe

export model=ufs.s2s

#hera 
export BASE=${BASE:-/home/Robert.Grumbine/rgdev/ice_scoring/}
if [ -z $BASE ] ; then
  echo WCOSS: BASE= /u/Robert.Grumbine/rgdev/ice_scoring/
  echo Hera:  BASE= /home/Robert.Grumbine/rgdev/ice_scoring/
  echo Orion: BASE= /u/rgrumbin/rgdev/ice_scoring/
  echo Gaea:  BASE= /ncrc/home1/Robert.Grumbine/rgdev/ice_scoring/
  echo Select one of these
  echo "  "
fi
echo BASE = $BASE

#Check the python environment -- assumes that path already references an appropriate interpreter 
. $HOME/rgdev/toolbox/misc/python_load.hera
if [ $? -ne 0 ] ; then
  echo you are missing necessary elements of the python environment.
  echo please install the needed modules and retry
  echo "    " If on hera, use a recent anaconda distribution, such as obtained by
  echo "    "   module use -a /contrib/anaconda/modulefiles
  echo "    "   module load anaconda/latest
  exit 1
fi
python3 ${BASE}/NCEP_si_verf/main_dir/checkenv.py

#Start copying elements over to carry out the evaluation
for f in contingency_plots.py collate.py 
do
  if [ ! -f $f ] ; then
    cp -p ${BASE}/NCEP_si_verf/concentration/$f .
  fi
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done
if [ ! -f runtime.def ] ; then
  cp -p ${BASE}/model_definitions/${model}.def runtime.def
fi

#for f in README verf_files.py setup_verf_ice.py platforms.py scores.py year.csh final.py all.csh 
for f in README verf_files.py setup_verf_ice.py platforms.py scores.py 
do
  if [ ! -f $f ] ; then
    cp -p ${BASE}/NCEP_si_verf/main_dir/$f .
  fi
  if [ ! -f $f ] ; then
    if [ -f ${BASE}/NCEP_si_verf/main_dir/shells/$f ] ; then
      cp -p ${BASE}/NCEP_si_verf/main_dir/shells/$f .
    else
      echo could not find $f in $BASE
      exit 1
    fi
  fi
done

export EXDIR=`pwd`
export EXBASE=`pwd`

#create and populate the exec directory if needed:
if [ ! -d ${BASE}/NCEP_si_verf/exec ] ; then
  cd ${BASE}
  ./makeall.sh
  if [ $? -eq 0 ] ; then
    echo copy exec dir from $BASE
    cp -rp ${BASE}/NCEP_si_verf/exec $EXDIR
  else
    echo failed to find or create execs, exiting now
    exit 2
  fi
else
  echo exec directory does exist in ${BASE}/exec
fi

cd $EXDIR
for d in exec 
do
  cp -rp ${BASE}/NCEP_si_verf/$d .
  if [ $? -ne 0 ] ; then
    echo error trying to copy $d from $BASE
    exit 4
  fi
  if [ ! -d $d ] ; then
    echo could not find directory $d in $BASE, exiting
    exit 4
  fi
done
if [ -d exec ] ; then
  cp -p runtime.def exec
fi


# tries to create fix directory link, but doesn't try hard
cd $EXDIR
if [ ! -d ${BASE}/fix ] ; then
  echo You must manually create the fix directory
  echo WCOSS: ln -sf /u/Robert.Grumbine/rgdev/fix .
  echo Hera:  ln -sf /home/Robert.Grumbine/rgdev/fix .
  echo Orion: ln -sf /u/rgrumbin/rgdev/fix .
  echo Gaea:  ln -sf /ncrc/home1/Robert.Grumbine/rgdev/fix .
  exit 3
fi
ln -sf $BASE/../fix .

#Check the directory / data environment for needed directories
python3 ${BASE}/NCEP_si_verf/main_dir/platforms.py trial
if [ $? -ne 0 ] ; then
  echo you need to correct the machines list and directory references in platforms.py
  exit 1
fi

if [ $? -eq 0 ] ; then
  echo successfully created the evaluation directory and stocked it with control files,
  echo   executables, and reference fixed files
fi
