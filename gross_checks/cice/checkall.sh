#!/bin/sh

source ../nest

n=0
while [ $n -lt 120 ] 
do
  echo n = $n
  time python3 evo_year.py $n gen4 > $n.out
  n=`expr $n + 1`
done
