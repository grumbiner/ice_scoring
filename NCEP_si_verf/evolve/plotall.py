import sys
import os
import csv
import copy

import numpy as np

#----------------------------------------------------
dates = np.zeros((365))
obs_nh = np.zeros((365))
obs_sh = np.zeros((365))
obs_glob = np.zeros((365))
mod_nh = np.zeros((365))
mod_sh = np.zeros((365))
mod_glob = np.zeros((365))

nstat = 9
ncand = 1200

def readin(fname, mod_nh, mod_sh, mod_glob):
  fin = open(fname,"r")
  k = 0
  for line in fin:
    l2 = line.replace('  ',' ')
    words = l2.split(' ')
    mod_nh[k] = float(words[4])
    mod_sh[k] = float(words[7])
    mod_glob[k] = float(words[10])
    k += 1
  fin.close()


import matplotlib
import matplotlib.pyplot as plt
def show(gen, species, obs_nh, obs_sh, obs_glob, mod_nh, mod_sh, mod_glob):
    #debug: print("plotting", flush=True)
  delta_nh = copy.deepcopy(obs_nh)
  delta_nh -= mod_nh
  gen_str = "{:d}".format(gen)
  spec_str = "{:d}".format(species)
  # plot the two
  fig,ax = plt.subplots()
  xticks = np.arange(1,365,30)
  ax.set_xticks(xticks)
  ax.set(xlabel = 'day of year ', ylabel = 'million km^2 extent')
  ax.set(title = 'Generation '+gen_str+' Species '+spec_str)
  ax.plot(dates, obs_nh, color="black", label="Observed NH")
  ax.plot(dates, mod_nh, color="blue", label="Model NH")
  ax.plot(dates, delta_nh, color="red", label="O-M NH")
  ax.legend()
  ax.grid()
  plt.savefig("nh_"+gen_str+"_"+spec_str+".png")
  plt.close()


# Get observations
nsidc = open("new.csv", "r")
obs = csv.reader(nsidc, delimiter=',')
k = 0
for line in obs:
  #debug: print(line[0], " ",line[1], flush=True)
  dates[k] = k+1
  obs_nh[k] = float(line[1])
  obs_sh[k] = float(line[2])
  obs_glob[k] = float(line[3])
  k += 1
nsidc.close()


#------  read in and transform (mean errors = abs(mean error)) 
#for gen in range(0,10):
for gen in range(0,2):

  for species in range(0,130):

    fname = "gen"+"{:d}".format(gen)+"/fout"+"{:d}".format(species)
    if (os.path.exists(fname) ):
      #debug: print("do something with ",fname, flush=True)
      readin(fname, mod_nh, mod_sh, mod_glob)
      show(gen, species, obs_nh, obs_sh, obs_glob, mod_nh, mod_sh, mod_glob)

    #debug: else:
      #debug:  print("nofile ",fname, flush=True)

    #debug: exit(0)

