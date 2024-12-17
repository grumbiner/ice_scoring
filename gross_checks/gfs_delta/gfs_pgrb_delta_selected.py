import os
import sys

import numpy as np

#import netCDF4
import pygrib

import bounders

#-----------------------------------------------------------------
# open bounds file (if possible)
try:
  fdic = open(sys.argv[1], "r")
except:
  print("could not find a dictionary file, exiting")
  exit(1)
bounds = bounders.bounds()
#debug: print(bounds, flush=True)

fname = sys.argv[2]
if (not os.path.exists(fname)):
  print("could not open ",fname)
  exit(1)

fn2   = sys.argv[3]
if (not os.path.exists(fn2)):
  print("could not open ",fn2)
  exit(1)

#debug: print("have all three files ",flush=True)

grbs = pygrib.open(fname)
grb2 = pygrib.open(fn2)
lats, lons = grbs[1].latlons()
nx = len(lats[0,:])
ny = len(lats[:,0])

tmask = np.zeros((ny, nx))
tarea = np.zeros((ny, nx))
#debug: print("nx ny lat lon ",nx, ny, lats.max(), lats.min(), lons.max(), lons.min() )
#debug: exit(0)

#grib level types
types = [ 'isobaricInPa', 'isobaricInhPa' ]

#levels : b (pgrb2b): 1, 2, 3, 5, 7, 125-875 by 50 
#levels : a (pgrb2) : 1, 2, 4, 7, 10, 20, 40, 70 -- isobaricInPa, not isobaricInhPa
#  isobaricInhPa: 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 70, 100-900 by 50, 900-1000 by 25
palevels = [1, 2, 4, 7, 10, 20, 40, 70 ]
hpalevels = [ 1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 70, 125, 175, 225, 
             275, 325, 375, 425, 525, 575, 625, 675, 725, 775, 825, 875, 
             100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 
             700, 750, 800, 850, 900, 925, 950, 975, 1000 ]

#short names of interest:
shorts=[ 'gh', 't', 'r', 'tcc', 'q', 'w', 'wz', 'u', 'v', 'absv', 'clwmr', 'icmr', 'rwmr', 'snmr', 'grle', 'o3mr' ]

grbindex = pygrib.index(fname, 'typeOfLevel', 'shortName', 'level')
grb2index = pygrib.index(fn2, 'typeOfLevel', 'shortName', 'level')


# Read through the dictionary for what variables we're interested in
errcount = 0
for line in fdic:
  words = line.split()
  sname = words[0]
  bounds.set(sname, words[1], words[2], words[3], words[4])

# skip the highest levels (0.7 mb and above)
  for lvl in hpalevels:
  #for lvl in [ 10, 500 ]:
    try:
      selected =  grbindex(typeOfLevel=types[1], shortName = sname, level = lvl)
      select2  = grb2index(typeOfLevel=types[1], shortName = sname, level = lvl)
      for i in range(0, len(selected)):
        delta = selected[i].values
        delta -= select2[i].values
        #debug: print(sname, lvl, types[1], 
        #debug:       selected[i].values.max(), selected[i].values.min(),
        #debug:       select2[i].values.max(), select2[i].values.min(),
        #debug:       delta.max(), delta.min(), flush=True )
        
        gfail = bounds.whether(delta)
        if (gfail):
          errcount += bounds.where(delta, lats, lons, tmask, tarea, level = lvl)
    except: 
      continue

print(errcount)
exit(0)

#-----------------------------------------------------------------
# read fout and determine what the name of the latitude and longitude variables are
#  also the mask and cellarea variables, if present
# ------------- below here should be generic to all systems -------------------

print("now trying dictionary and bootstrap files")

dictionary_file = "beta"
bootstrap_file  = "boot_out"
tbound = tmp.bootstrap(dictionary_file, bootstrap_file, orig)
#  The following isn't needed, as the output will be sent to bootstrap_file already.
#for i in range (0,len(tbound)):
#  tbound[i].show()

orig.close()

#exit(0)

#note:
#  Nonvalues might actually be printed to the bootstrap_file, need to edit.

#third iteration of the program is to just read in a boostrap file for all values:
print("third iteration")
orig = netCDF4.Dataset(fname, "r") 
lats = orig.variables[name_of_latitudes][:,:]
lons = orig.variables[name_of_longitudes][:,:]

try:
  tmask = orig.variables[name_of_landmask][:,:]
except:
  tmask = np.zeros((ny, nx))

try:
  tarea = orig.variables[name_of_cellarea][:,:]
except:
  tarea = np.zeros((ny, nx))
  tarea = 1.0

tbound = tmp.readin(dictionary_file, orig)
