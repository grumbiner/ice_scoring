import sys
#viewing cProfile output from
#python3 -m cProfile -o prof.stats icing.py
import pstats

p = pstats.Stats(sys.argv[1])
#p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('time').print_stats(20)
