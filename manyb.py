from pegpy.gparser.cython_gpeg import cgpeg
from pegpy.tpeg import grammar
from pathlib import Path
import time
import pstats, cProfile

import pyximport
pyximport.install()

manyb = grammar('manyb.gpeg')
print(manyb)
parser = cgpeg(manyb)

bs = 'b' * 100

cProfile.runctx("parser(bs)", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()

start_time = time.perf_counter()
ast = parser(bs)
execution_time = time.perf_counter() - start_time
print(f'time: {execution_time}')
# print(f'ast: {ast}')
