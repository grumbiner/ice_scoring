#!/bin/sh

# skip gh to avoid 'high max' or 'high min'

for f in t q w wz u v o3mr absv clwmr icmr rwmr snmr grle 
do
  grep "$f " all.c | grep pm | sort -nr -k 4 > all.c.$f
  grep "$f " all.d | grep pm | sort -nr -k 4 > all.d.$f
done
grep -v absv all.c.v > v; mv v all.c.v
grep -v absv all.d.v > v; mv v all.d.v

for f in t q w wz u v o3mr absv clwmr icmr rwmr snmr grle 
do
  cat all.c.$f all.d.$f | sort -nr -k 4 > $f
done
