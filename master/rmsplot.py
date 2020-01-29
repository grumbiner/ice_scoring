import csv
import numpy as np
import matplotlib

lead = np.zeros((35))
rmse = np.zeros((35))
with open('fvn.csv') as csvfile:
  sreader = csv.reader(csvfile, delimiter=',')
  k = 0
  for line in sreader:
    lead[k] = k+1
    rmse[k] = line[1]
    #print(line[0],' ',k+1,' ',line[1])
    print(lead[k], ' ',rmse[k])
    k += 1

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set(xlabel='Lead time, days', ylabel = 'edge rms (km)')
ax.set(title='Forecast vs observation edge location rms (km)')
ax.plot(lead,rmse)
ax.grid()
fig.show()
#matplotlib.pyplot.savefig("test.png")
plt.savefig("test.png")

