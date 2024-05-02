import os
import sys
import datetime
from math import *
#debug: print("importing external modules",flush=True)

import numpy as np
import numpy.ma as ma
#debug: print("imported numpy",flush=True)

import netCDF4
#debug: print("Finished importing external modules",flush=True)

import bounders
#debug: print("Finished importing private  modules",flush=True)

#---------------------------------------------------
SCORING=os.environ['SCOREDIR']
fin = open(SCORING+'/model_definitions/cice.header','r')


ctl_dict = SCORING+'/gross_checks/ctl/cice.evo'
flying_dict = 'alpha'

# new management of header variable names
headers = {
  'nx' : '',
  'ny' : '',
  'TLON' : '',
  'TLAT' : '',
  'tmask' : '',
  'tarea' : ''
}

k = 0
for line in fin:
    #debug: print(k, len(line), flush=True)
  if (len(line) < 3):
      #debug: print("zero length line",flush=True)
      break
  words = line.split()
  #debug: print(k, words[0], flush=True)
  headers[words[0]] = words[1]
  k += 1
#debug: print(headers, flush=True)
#debug: exit(0)

ICE_BASE='/ncrc/home1/Robert.Grumbine/scratch/CICE_RUNS/'
#EXPT_BASE='gaea_intel_smoke_gx3_4x1_diag1_evo0_evolength_yr_out.evo/'
testid='gen2'
pno = sys.argv[1]
EXPT_BASE='gaea_intel_smoke_gx3_1x1_evo'+pno+'_med3_yr_out.'+testid
ICE_RUNDIR=ICE_BASE+EXPT_BASE+'/history'
fout = open('fout'+pno+'.'+testid,"w")

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
#Robert Grumbine
#30 January 2020
#
#data file = fname
#control dictionary = control dictionary
#bootstrapped dictionary = alpha (optional, may be written to if needed and present)
#---------------------------------------------------

errcount = int(0)
ngfail   = int(0)

dt    = datetime.timedelta(1)
start = datetime.datetime(2005,1,1)
end   = datetime.datetime(2005,12,31)
tag   = start

while (tag <= end):
  yy = tag.strftime("%Y")
  mm = tag.strftime("%m")
  dd = tag.strftime("%d")
  fname = ICE_RUNDIR+"/iceh."+yy+'-'+mm+'-'+dd+'.nc'

#---------------------------------------------------
  if (os.path.exists(fname) ):
    model = netCDF4.Dataset(fname, 'r')
    nx = len(model.dimensions[headers['nx']])
    ny = len(model.dimensions[headers['ny']])
    
    # if tag == start: (invariants through run)
    #rg q: is this universal across UFS? -- no.
    tlons = model.variables[headers["TLON"]][:,:]
    tlats = model.variables[headers["TLAT"]][:,:]
    
    #LAND = 0, #Ocean = 1
    try:
      tmask = model.variables[headers["tmask"]][:,:]
    except :
      tmask = np.zeros((ny, nx))
      tmask = 1.

    tarea = model.variables[headers["tarea"]][:,:]

    #Get the dictionary file, perhaps with bounds given
    try:
      fdic = open(ctl_dict)
    except:
      print("could not find a dictionary file ",ctl_dict, flush=True)
      exit(1)

    try: 
      flying_dictionary = open(flying_dict,"w")
      flyout = True
    except:
      #debug: print("cannot write out to bootstrap dictionary file", flush=True)
      flyout = False
    #------------ end of getting header and reference figures ---------

    parmno = 0
    for line in fdic:
      words = line.split()
      #debug: print(len(words), words, flush=True)
      parm = words[0]
      tmp = bounders.bounds(param=parm)
      try: 
        temporary_grid = model.variables[parm][0,:,:]
      except:
        #debug: print(parm," not in data file", flush=True)
        continue
  
      # find or bootstrap bounds -----------------
      tmp.set_bounds(temporary_grid, words, flyout, flying_dictionary)
  
      #Global tests -- test whether the test fails anywhere
      gfail = tmp.whether(temporary_grid)
  
      #Pointwise checks -- Show where (and which) absolute max/min test failed:
      if (gfail):
        ngfail += 1
        errcount += tmp.where(temporary_grid, tlats, tlons, tmask, tarea, fout = fout)
  
      parmno += 1
    # ---- end of reading through ctl file and checking parms

    print(tag.strftime("%Y%m%d"),"errcount, gfails = ",errcount, ngfail, file = fout)

  tag += dt
  model.close()


#------------------------------------------------------
#exit codes are bounded, while error counts are not
if (errcount == 0):
  exit(0)
else:
  exit(1)
