#!/bin/sh

for f in gh t q w wz u v o3mr absv clwmr icmr rwmr snmr grle 
do
  grep "$f " all.a | sort -nr -k 4 > all.a.$f
  grep "$f " all.b | sort -nr -k 4 > all.b.$f
done
grep -v absv all.a.v > v; mv v all.a.v
grep -v absv all.b.v > v; mv v all.b.v

for f in gh t q w wz u v o3mr absv clwmr icmr rwmr snmr grle 
do
  cat all.a.$f all.b.$f | sort -nr -k 4 > $f
done
