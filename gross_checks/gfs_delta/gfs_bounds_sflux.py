import os
import sys
import datetime
from math import *

import numpy
import numpy.ma as ma

import pygrib

import bounders

# Variables to work on:
vars = [ '2t' ,'2sh' ,'10u' ,'10v' ,'lsm' ,'lhtfl' ,'ishf' ,'mslhf' ,'msshf' ,'uswrf' ,'ulwrf' ,'dswrf' ,'utaua' ,'vtaua' ,'fsr' ,'sithick' ,'ci' ,'al' ]

# open ctrl + expt grib files (sflux)
ctrl = pygrib.open("ctrl.grib2")
expt = pygrib.open("expt.grib2")

#RG: get lons, lats of grib file:
lats, lons = ctrl[1].latlons()
ny = len(lats[:,0])
nx = len(lats[0,:])
#debug: print("latlon info ", lats.max(), lats.min(), lons.max(), lons.min() )
#debug: x = ctrl[1].values
#debug: print("nx, ny = ",nx, ny, flush=True)
tmask = numpy.zeros((ny, nx))
tarea = numpy.zeros((ny, nx))
#debug: exit(0)


# open bounds file (if possible)
try: 
  fdic = open(sys.argv[1])
except:
  print("could not find a dictionary file, exiting")
  exit(1)
bounds = bounders.bounds()

# loop over all keys of interest in the delta control file and look
#   at differences between ctrl and difference 

errcount = 0
for line in fdic:
    #debug: print(line, flush=True)
    words = line.split()
    #debug: print(words, len(words), flush=True)
    parm = words[0]

    bounds.set(parm, words[2], words[1], words[4], words[3])

    cindex = ctrl(shortName = parm)
    eindex = expt(shortName = parm, typeOfLevel = cindex[0].typeOfLevel)
   
    x     = cindex[0]
    delta = cindex[0].values
    delta -= eindex[0].values


    gfail = bounds.whether(delta)
    #debug: print("parm = ", parm, "gfail = ",gfail, flush=True)
    if (gfail):
        #debug: print(x.shortName, x.values.max(), x.values.min(), 
        #debug:  delta.max(), delta.min(), 
        #debug:  (delta.max() - delta.min()) / (x.values.max() - x.values.min()), 
        #debug:  flush=True)

      errcount += bounds.where(delta, lats, lons, tmask, tarea)

print("total of ", errcount, "errors identified")
