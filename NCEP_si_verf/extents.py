import os
import sys
import csv
import datetime
import copy 

import numpy as np


dates = []
obs_nh = np.zeros((365))
obs_sh = np.zeros((365))
obs_glob = np.zeros((365))
mod_nh = np.zeros((365))
mod_sh = np.zeros((365))
mod_glob = np.zeros((365))

# Get observations
nsidc = open("new.csv", "r")
obs = csv.reader(nsidc, delimiter=',')
k = 0
for line in obs:
  #debug: print(line[0], " ",line[1], flush=True)
  dates.append(line[0])
  obs_nh[k] = float(line[1])
  obs_sh[k] = float(line[2])
  obs_glob[k] = float(line[3])
  k += 1
nsidc.close()
#debug: print(obs_nh.mean(), obs_sh.mean(), obs_glob.mean(), flush=True )
  
# Get model:
def getmod(mod_nh, mod_sh, mod_glob, model):
  k = 0
  for line in model:
    l2 = line.replace('  ',' ')
    words = l2.split(' ')
    #debug: for i in range(0,15):
      #debug: print(i,words[i])
    #debug: exit(0)
    #debug: print(words[0], " ",words[4], flush=True)
    mod_nh[k] = float(words[4])
    mod_sh[k] = float(words[7])
    mod_glob[k] = float(words[10])
    k += 1
#debug: print(mod_nh.mean(), mod_sh.mean(), mod_glob.mean(), flush=True )

# --------- End getting data --------------------------
def eval_mod(obs_nh, mod_nh, obs_sh, mod_sh, obs_glob, mod_glob, nmod):
  # mean errors, rms
  # mean absolute error
  # annual harmonics 1-4
  #
  delta_nh = copy.deepcopy(obs_nh)
  delta_nh -= mod_nh
  d2 = np.abs(delta_nh)
  #print(nmod, "nh mean std mae: ",delta_nh.mean(), delta_nh.std(), d2.mean() )
  
  delta_sh = copy.deepcopy(obs_sh)
  delta_sh -= mod_sh
  ds2 = np.abs(delta_sh)
  #print(nmod, "sh mean std mae: ",delta_sh.mean(), delta_sh.std(), ds2.mean() )
  
  delta_glob = copy.deepcopy(obs_glob)
  delta_glob -= mod_glob
  dg2 = np.abs(delta_glob)
  #print(nmod, "gl mean std mae: ",delta_glob.mean(), delta_glob.std(), dg2.mean() )
  
  print(nmod, "nh, sh, glob; mean, std, mae: ",
        "{:.3f}".format(delta_nh.mean()), "{:.3f}".format(delta_nh.std()), "{:.3f}".format(d2.mean()) ,
        "{:.3f}".format(delta_sh.mean()), "{:.3f}".format(delta_sh.std()), "{:.3f}".format(ds2.mean()) ,
    "{:.3f}".format(delta_glob.mean()), "{:.3f}".format(delta_glob.std()), "{:.3f}".format(dg2.mean()) )
  
  # plot the two
  import matplotlib
  import matplotlib.pyplot as plt
    
  #fig,ax = plt.subplots()
  #ax.set(xlabel = 'date ', ylabel = 'million km^2 extent')
  #ax.plot(dates, delta_nh)
  #ax.grid()
  #plt.savefig("nh.png")

# --------- End evaluating data --------------------------

for i in range(0, 120):
  #fname="gen4.15/fout"+"{:d}".format(i)
  fname="~/scratch/CICE_RUNS/generation3/fout"+"{:d}".format(i)
  try: 
    model = open(fname, "r")
    getmod(mod_nh, mod_sh, mod_glob, model)
    model.close()
    eval_mod(obs_nh, mod_nh, obs_sh, mod_sh, obs_glob, mod_glob, i)
    #debug: print(i, obs_nh.mean(), mod_nh.mean(), flush=True )
  except:
    print("species ",i,"was a fatal variation")


