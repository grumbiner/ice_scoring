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
# new management of header variable names
headers = {
  'nx' : '',
  'ny' : '',
  'TLON' : '',
  'TLAT' : '',
  'tmask' : '',
  'tarea' : ''
}

SCORING=os.environ['SCOREDIR']
fin = open(SCORING+'/model_definitions/cice.header','r')
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

#---------------------------------------------------
#Gross bound checks on .nc files, developed primarily from the sea ice (CICE6) output
#Robert Grumbine
#30 January 2020
#
#data file = argv[1] (input)
#control dictionary = argv[2] (input)
#bootstrapped dictionary = argv[3] (optional, may be written to if needed and present)
#---------------------------------------------------

errcount = int(0)
ngfail   = int(0)

if (not os.path.exists(sys.argv[1]) ):
  print("failure to find ",sys.argv[1], flush=True)
  exit(1)
else:
  model = netCDF4.Dataset(sys.argv[1], 'r')
  nx = len(model.dimensions[headers['nx']])
  ny = len(model.dimensions[headers['ny']])
  
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
    fdic = open(sys.argv[2])
  except:
    print("could not find a dictionary file ",sys.argv[2], flush=True)
    exit(1)

  try: 
    flying_dictionary = open(sys.argv[3],"w")
    flyout = True
  except:
    #debug: print("cannot write out to bootstrap dictionary file", flush=True)
    flyout = False

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

    #Pointwise checks -- Show where (and which) test failed:
    if (gfail):
      ngfail += 1
      errcount += tmp.where(temporary_grid, tlats, tlons, tmask, tarea)

    parmno += 1

#exit codes are bounded, while error counts are not
print(sys.argv[1],"errcount, gfails = ",errcount, ngfail)
if (errcount == 0):
  exit(0)
else:
  exit(1)
