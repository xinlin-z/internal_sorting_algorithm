import os
from ctypes import *
import random
import time
import numpy as np
from functools import partial
from common import shell, cprint
from timeit import timeit


# measure process time, run only one time
tit = partial(timeit, timer=time.process_time, number=1)


print('# test sort time (cpu) with same data:')
print(shell('gcc -Wall -Wextra -fPIC -shared -std=c99'
            ' -O3 common.c sort.c -o sort.so'))
sort = CDLL('./sort.so')


size_int = sizeof(c_int)
size_t = sizeof(c_size_t)
print('sizeof(int) =', size_int)
print('sizeof(size_t) =', size_t)


libc = CDLL('libc.so.6')
sorts = [
    ('bubble',            sort.bubble),
    ('selects',           sort.selects),
    ('insert',            sort.insert),
    ('insert2',           sort.insert2),
    ('binsert',           sort.binsert),
    ('binsert2',          sort.binsert2),
    ('merge',             sort.merge),
    ('shell',             sort.shell),
    ('shell2',            sort.shell2),
    ('merge_r',           sort.merge_r),
    ('quick',             sort.quick),
    ('heapify',           sort.heapify),
    ('radix',             sort.radix),
    ('btree',             sort.btree),
    ('count',             sort.count),
    ('sorted(python)',    sorted),
    ('list.sort(python)', list.sort),
    ('np.sort(numpy)',    np.sort),
    ('qsort(glibc)',       libc.qsort),
]
random.shuffle(sorts)


def run(data):

    def __cr(ret):
        nonlocal r
        r = ret

    result = []
    failed = []
    for i in range(len(sorts)):
        # prep data
        cd = (c_int*len(data))(*data)
        dcd = byref(cd)
        f = sorts[i][1]
        d2t = {'f':f,'cd':cd,'dcd':dcd,'__cr':__cr}
        fn = sorts[i][0]
        # call
        r = -1  # return value
        t = 0
        if fn in ('bubble', 'selects', 'insert', 'insert2',
                  'binsert', 'binsert2', 'shell', 'shell2', 'heapify'):
            t = tit('f(dcd,len(cd))', globals=d2t)
        elif fn in ('merge', 'radix', 'btree'):
            t = tit('__cr(f(dcd,len(cd)))', globals=d2t)
            if r != 0:
                failed.append((fn, 'E:%d'%r))
                continue
        elif fn in ('merge_r'):
            t = tit('__cr(f(dcd,0,len(cd)-1))', globals=d2t)
            if r != 0:
                failed.append((fn, 'E:%d'%r))
                continue
        elif fn in ('quick'):
            t = tit('f(dcd,0,len(cd)-1)', globals=d2t)
        elif fn in ('count'):
            mem_limit = c_size_t(1024**3)  # 1G memory
            d2t['mem_limit'] = mem_limit
            t = tit('__cr(f(dcd,len(cd),mem_limit))', globals=d2t)
            if r != 0:
                failed.append((fn, 'E:%d'%r))
                continue
        elif fn in ('qsort(glibc)'):
            d2t['size_int'] = size_int
            d2t['cmp_int'] = sort.cmp_int
            t = tit('f(dcd,len(cd),size_int,cmp_int)', globals=d2t)
        elif fn in ('sorted(python)','list.sort(python)','np.sort(numpy)'):
            d2t['dd'] = list(cd)
            t = tit('f(dd)', globals=d2t)
        else:
            assert False
        # assert
        if fn not in ('sorted(python)','list.sort(python)','np.sort(numpy)'):
            assert list(cd) == sorted(data)
        # record success
        result.append((fn, t))
    # sort result and print
    result.sort(key=lambda x:x[1])
    cprint(' '*4, 'Algo Name'.ljust(24,' '), 'Time(s)'.center(13, ' '),
           fg='c', style='inverse')
    for i,it in enumerate(result):
        print(str(i+1).ljust(4,' '),it[0].ljust(24,' '),'%.10f'%it[1])
    # print failed
    for j,it in enumerate(failed):
        cprint(str(j+1+i+1).ljust(4,' '), it[0].ljust(24,' '), it[1],
               fg='k', bg='m', style='blink')


# data1
data = []
dsize = 200000
for i in range(dsize):
    data.append(random.randint(-500,500))
print(f'Data1: {dsize} integers in random from -500 to 500 (many duplicated)')
run(data)
print()

# data2
data = []
dsize = 200000
assert size_int == 4
a = int.from_bytes(b'\x80\x00\x00\x00', 'big', signed=True)
b = int.from_bytes(b'\x7f\xff\xff\xff', 'big', signed=True)
for i in range(dsize):
    data.append(random.randint(a,b))
print(f'Data2: {dsize} integers in random from {a} to {b}')
run(data)
print()

# test over, delete
os.remove('sort.so')

