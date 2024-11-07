import os
import sys
import datetime
from math import *

import numpy
import numpy.ma as ma

import pygrib

import bounders

#----------------------------------------------------------
# open ctrl + expt grib files (pgrb2)
ctrl = pygrib.open("ctrl.grib2")
expt = pygrib.open("expt.grib2")

# open bounds file (if possible)
try: 
  fdic = open(sys.argv[1])
except:
  print("could not find a dictionary file, exiting")
  print("develop a bootstrap!")
  exit(1)

#----------------------------------------------------------

# loop over all keys in ctrl and difference with expt
for x in ctrl:
    delta = x.values
    index = expt(shortName = x.shortName, typeOfLevel = x.typeOfLevel)
    if (len(index) == 1):
        delta -= index[0].values
        print(x.shortName, x.values.max(), x.values.min(), 
              delta.max(), delta.min(), 
              (delta.max() - delta.min()) / (x.values.max() - x.values.min()), 
              flush=True)
    else:
        print(x.ShortName, len(index), x.typeOfLevel)


