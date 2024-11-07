import os
import sys

import numpy as np

#import netCDF4
import pygrib

import bounders

#-----------------------------------------------------------------
tmp = bounders.bounds()
fname = sys.argv[1]
if (not os.path.exists(fname)):
  print("could not open ",fname)
  exit(1)

fn2   = sys.argv[2]
if (not os.path.exists(fn2)):
  print("could not open ",fn2)
  exit(1)

#Perform an initial scan of some file and write out the information 
fout = open("alpha","w")

grbs = pygrib.open(fname)
grb2 = pygrib.open(fn2)
#debug: print("grbs = ",grbs, flush=True)

#debug: for x in grbs:
#debug:  print(x.shortName, x.typeOfLevel, x.level, x.name)

#type: isobaricInhPa
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

# try the upper atmosphere first (levels isobaricInPa, vs. isobaricInhPa)
#leveltype = types[0]
for sname in shorts:
#  for lvl in palevels:
#    try:
#      selected =  grbindex(typeOfLevel=types[0], shortName = sname, level = lvl)
#      select2  = grb2index(typeOfLevel=types[0], shortName = sname, level = lvl)
#      for i in range(0, len(selected)):
#        delta = selected[i].values
#        delta -= select2[i].values
#        print(sname, lvl, types[0], 
#              selected[i].values.max(), selected[i].values.min(),
#              select2[i].values.max(), select2[i].values.min(),
#              delta.max(), delta.min() )
#    except: 
#      continue
#
# for deeper levels
  for lvl in hpalevels:
    try:
      selected =  grbindex(typeOfLevel=types[1], shortName = sname, level = lvl)
      select2  = grb2index(typeOfLevel=types[1], shortName = sname, level = lvl)
      for i in range(0, len(selected)):
        delta = selected[i].values
        delta -= select2[i].values
        print(sname, lvl, types[1], 
              selected[i].values.max(), selected[i].values.min(),
              select2[i].values.max(), select2[i].values.min(),
              delta.max(), delta.min() )
    except: 
      continue


exit(0)

#-----------------------------------------------------------------
# read fout and determine what the name of the latitude and longitude variables are
#  also the mask and cellarea variables, if present
# also need an ncdump t0 determine nx, ny 
# copy and edit alpha to beta
# now look at what the extrema should be
orig = netCDF4.Dataset(fname, "r") 

#  This stage takes some manual inspection of the above output file
#Dimensions:
name_of_x_direction = "ni" #longitudes, nx
name_of_y_direction = "nj" #latitudes, ny
# Names of special grids:
name_of_latitudes  = "TLAT"
name_of_longitudes = "TLON"
name_of_landmask   = "tmask"     # can run without one
name_of_cellarea   = "tarea"     # can run without one
# ------------- below here should be generic to all systems -------------------


nx = orig.dimensions[name_of_x_direction].size
ny = orig.dimensions[name_of_y_direction].size
lats = orig.variables[name_of_latitudes][:,:]
lons = orig.variables[name_of_longitudes][:,:]
print(nx , "nx")
print(ny , "ny")

try:
  tmask = orig.variables[name_of_landmask][:,:]
except:
  tmask = np.zeros((ny, nx))

try:
  tarea = orig.variables[name_of_cellarea][:,:]
except:
  tarea = np.zeros((ny, nx))
  tarea = 1.0


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
