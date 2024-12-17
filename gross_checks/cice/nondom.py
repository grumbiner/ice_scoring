import sys
import os
import csv

import numpy

#--------------------------------------------
def known(name, candidates):
  result = False
  for i in range(0,len(candidates)):
    if (name == candidates[i][0]):
      result = True
      return result
  return result

def dominated(item, candidates):
  dom = False
  for i in range(0, len(candidates)):
    if (item[1] > candidates[i][1] and (item[2] > candidates[i][2])):
      dom = True
  return (dom)

def is_nondom(item, candidates):
  nondom1 = False
  nondom2 = False
  for i in range(0, len(candidates)):
    if (item[1] <= candidates[i][1]):
      nondom1 = True
      return True
    if (item[2] <= candidates[i][2]):
      nondom2 = True
      return True
  return (nondom1 or nondom2)
#--------------------------------------------


fin = open(sys.argv[1], "r")

names = ['']*100
errs = numpy.zeros((100))
gfail = numpy.zeros((100))

#------  read in 
k = 0
for line in fin:
  words = line.split(';')
  names[k] = words[0]
  errs[k]  = int(words[1])
  gfail[k] = int(words[2])
  k += 1
nexpt = k
# for these, lower is better
emin = errs[0:nexpt].min()
gmin = gfail[0:nexpt].min()

# ----- append candidates as good as the best on one or the other measure ----
cands = []
nc = 0
for k in range(0,nexpt):
  if (errs[k] == emin):
      #debug: print(names[k], errs[k], gfail[k])
    cands.append( [names[k], errs[k], gfail[k] ] )
    nc += 1
  if (gfail[k] == gmin):
      #debug: print(names[k], errs[k], gfail[k])
    cands.append( [names[k], errs[k], gfail[k] ] )
    nc += 1
#debug: print("nc = ",nc,cands[0][2])

#---------------------------------------------------------------
for k in range(0,nexpt):
  if (not known(names[k], cands) and is_nondom( [names[k], errs[k], gfail[k] ], cands) ): 
    if (not dominated( [names[k], errs[k], gfail[k] ], cands) ):
      cands.append( [names[k], errs[k], gfail[k] ] ) 
    #else:
    #  print("no ",names[k], errs[k], gfail[k] )
#print('nexpt, ncands ',nexpt, len(cands) )

#---------------------------------------------------------------
for k in range(0, len(cands) ):
  #print(' nondominated ', k, names[k], errs[k], gfail[k] )
  print(k, cands[k][0], cands[k][1], cands[k][2])
