import sys
import datetime

#-----------------------------------------------------------------------
#Evaluate the unix environment
import eval_unix_env
env = eval_unix_env.runtime_environment("", "", "")
if (env.ok_env() != 0 ):
  print("something wrong in unix environment",flush=True)
  exit(1)
else:
  print("valid unix environment", flush=True)
#debug: print("exbase, exdir, fixdir:",x.exbase, flush=True)


#Evaluate the platform ------ this creates some utility variables 
#                             specialized to this environment ------------
import platforms

x = platforms.machine.dirs
#debug: print(x['imsdir'], flush=True)
#debug: print(platforms.imsverf, flush=True)
if not (platforms.imsverf or platforms.nsidcverf or platforms.ncepverf or platforms.osiverf) : 
  raise Exception ("no valid verification sources, exiting")

  
#Check for verification data and import the 'gridded' class ----------
import verf_files

ims   = verf_files.ims()
nsidc = verf_files.nsidc_nh()
osisaf = verf_files.osisaf()
ncep   = verf_files.ncep()

#Find the forecast model -- specialized 'gridded' member -------------

import forecast_files

fcst = forecast_files.hr3b()

#----------------------------------------------------------------------
# Import scoring tools
from scores import *

#----------------------------------------------------------------------
# Now ready to loop over forecasts

# HR3b, HR4, HR5 all using a winter and a summer season's forecasts
#Winter
start = datetime.datetime(2019,12,3)
end   = datetime.datetime(2020,2,25)
#Summer
#start = datetime.datetime(2020,6,1)
#end   = datetime.datetime(2020,8,30)
dt = datetime.timedelta(3)
dt1 = datetime.timedelta(1)

tag = start
exdir = env.exdir
fixdir = env.fixdir

while (tag <= end):
  print(tag)
  #fcstdir = "/home/Robert.Grumbine/clim_data/hr3b/gfs." + tag.strftime("%Y%m%d") + "/00/model_data/ice/history/"
  fcstdir = "/home/Robert.Grumbine/clim_data/hr4/gfs." + tag.strftime("%Y%m%d") + "/00/model/ice/history/"
  valid = tag
  for hr in range(6,384,24):
    #debug: print(hr, valid, flush=True)

    tmp = fcst.get_grid(hr, fcstdir) 
    if (tmp != 0):
      valid += dt1
      continue

    obs = 0
#    if (platforms.ncepverf):
#      obs += ncep.get_grid(tag, x['ncepdir'])

#    if (platforms.imsverf):
#      obs += imsverf.get_grid(tag, x['imsdir'])

    if (platforms.nsidcverf):
      obs += nsidc.get_grid(tag, x['nsidcdir'])

#    if (platforms.osiverf):
#      obs += osisaf.get_grid(tag, x['osisafdir'])

    #debug: print("obs retcode sum", obs)

# Now tailor to concentration verification:
    if (platforms.nsidcverf):
      score_nsidc(fcst, nsidc, fcstdir, x['nsidcdir'], tag, valid, hr, exdir, fixdir)
    else:
      print("could not score concentration for ",fcst_dir,
             x['nsidcdir'], initial_date, valid_date, flush=True)

    
# For edges  RG: tripole cice currently bonkers
    #fcst.make_edge(tag, hr, fcstdir, x['edgedir'], exdir, fixdir)

    valid += dt1

  tag += dt
