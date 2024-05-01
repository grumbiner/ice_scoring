#!/bin/sh
#
n=0
while [ $n -lt 100 ] 
do
  echo n = $n
  time python3 evo_year.py $n > $n.out
  n=`expr $n + 1`
done
