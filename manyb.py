from pegpy.gparser.cython_gpeg import cgpeg
from pegpy.tpeg import grammar
from pathlib import Path
import time

manyb = grammar('manyb.gpeg')
print(manyb)
parser = cgpeg(manyb)
start_time = time.perf_counter()
ast, option = parser('bbbbbbbbbbb')
execution_time = time.perf_counter() - start_time
print(f'time: {execution_time}')
# print(f'ast: {ast}')
# print(option)
