#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in icec icetk land tisfc snod ugrd10m vgrd10m ulwrf dlwrf uflx_ave vflx_ave shtfl lhtfl spfh2m
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
  wc ${f}.s
done

