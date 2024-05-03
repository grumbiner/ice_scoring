import os
import datetime


# -- universal environmental settings
FIXDIR='/ncrc/home1/Robert.Grumbine/rgref/fix/'
EXDIR='/ncrc/home1/Robert.Grumbine/rgdev/ice_scoring/NCEP_si_verf/exec/'
OUTDIR='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/'

start = datetime.date(2005,1,1)
end   = datetime.date(2005,12,31)
dt = datetime.timedelta(1)

acrit = 0.0

# specific to given experiments
#EXPT='reference.evo0'
GEN='gen1'

for evo in range(0,99):
  tag   = start
  #debug: print("trying experiment ",evo, flush=True)

  sno="{:d}".format(evo)
  EXPT='generation1/gaea_intel_smoke_gx3_1x1_evo'+sno+'_med3_yr_out.'+GEN
  fname = 'fout'+sno

  fout = open(fname,'w')
  while (tag <= end):
    dtag=tag.strftime("%Y-%m-%d")
    cmd = EXDIR+'/cice_solo '+FIXDIR+'/seaice_gland5min '+OUTDIR+EXPT+ '/history/iceh.'+dtag+'.nc '+"{:.3f}".format(acrit) + ' ' + dtag + " >> "+ fname
    #debug: print(tag," ",end="", file = fout, flush=True)
    #debug: print(tag,flush=True)
    os.system(cmd)
    tag += dt
  fout.close()

