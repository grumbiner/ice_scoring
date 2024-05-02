#!/bin/sh

source ../nest

n=0
while [ $n -lt 94 ] 
do
  echo n = $n
  time python3 evo_year.py $n > $n.out
  n=`expr $n + 1`
done
