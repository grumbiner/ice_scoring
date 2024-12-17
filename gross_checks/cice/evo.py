import os
import sys
import datetime

ICE_BASE='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/'
EXPT_BASE='gaea_intel_smoke_gx3_4x1_diag1_evo0_evolength_yr_out.evo/'

ICE_RUNDIR=ICE_BASE+EXPT_BASE+'/history'
SCORING=os.environ['SCOREDIR']


dt    = datetime.timedelta(1)
start = datetime.datetime(2005,1,1)
end   = datetime.datetime(2005,12,31)
tag   = start

while (tag <= end):
  yy = tag.strftime("%Y")
  mm = tag.strftime("%m")
  dd = tag.strftime("%d")
  fname = ICE_RUNDIR+"/iceh."+yy+'-'+mm+'-'+dd+'.nc'
  if (os.path.exists(fname)):
    print("python3 cice.py ",fname,SCORING+"/gross_checks/ctl/cice.evo alpha > out."+tag.strftime("%Y%m%d") )

  tag += dt

