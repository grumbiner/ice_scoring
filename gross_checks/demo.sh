
#Model specific names of grid specifications are in 2nd argument (cice.header here)
#Model variable names and their bounds are in ctl/icesubset.high (here)
#'beta' is an optional argument, useful when bounds are unknown but variable names are

export MODDEF=../model_definitions
python3 universal2d.py a.nc cice.header ctl/icesubset.high beta
