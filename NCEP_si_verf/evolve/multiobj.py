# --- sample for 2 parameters -----
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

# -- versions for multimetric --------
def dominates(ref, cand):
    #RG: true if nbetter == nparm
    return True
def dominated_by(ref, cand):
    #RG: true if nbetter == 0
    return True
def nondom(ref, cand):
    #RG: true if nbetter > 0
    return True
#return # of metrics candidate is better than the reference on.
def check(ref, cand, toler = 1.0):
    nbetter = 0
    for k in range (0, len(cand[2])):
        #if (cand[2][k] < ref[2][k]):
        if (cand[2][k] < toler*ref[2][k]):
            nbetter += 1
    return nbetter
# use a list of references to check, as in a set from orthogonalization: 
def checklist(ref, cand, orth):
    nbetter = 0
    for k in range (0, len(cand[2])):
      if (k in orth):
        if (cand[2][k] < ref[2][k]):
            nbetter += 1
    return nbetter
