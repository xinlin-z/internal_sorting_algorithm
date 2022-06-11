# internal_sorting_algorithm
Internal sorting algorithm implementated by C, tested and compared by Python.

# unit test

``` shell
$ python3 utest.py -v

# common.c:
sizeof(int) =  4
sizeof(size_t) =  8

test_cmp_int (__main__.test_common_c) ... ok
test_max_int (__main__.test_common_c) ... ok
test_min_int (__main__.test_common_c) ... ok

# sort.c:
sizeof(int) =  4
sizeof(size_t) =  8

test_binsert (__main__.test_sort_c) ... ok
test_binsert2 (__main__.test_sort_c) ... ok
test_btree (__main__.test_sort_c) ... ok
test_bubble (__main__.test_sort_c) ... ok
test_count (__main__.test_sort_c) ... ok
test_get_max (__main__.test_sort_c) ... ok
test_get_min (__main__.test_sort_c) ... ok
test_get_radix (__main__.test_sort_c) ... ok
test_heapify (__main__.test_sort_c) ... ok
test_insert (__main__.test_sort_c) ... ok
test_insert2 (__main__.test_sort_c) ... ok
test_merge (__main__.test_sort_c) ... ok
test_merge_r (__main__.test_sort_c) ... ok
test_quick (__main__.test_sort_c) ... ok
test_radix (__main__.test_sort_c) ... ok
test_selects (__main__.test_sort_c) ... ok
test_shell (__main__.test_sort_c) ... ok
test_shell2 (__main__.test_sort_c) ... ok
test_split_np (__main__.test_sort_c) ... ok

----------------------------------------------------------------------
Ran 22 tests in 12.844s

OK
```

# speed test

``` shell
$ python3 test_sort_time.py
# test sort time (cpu) with same data:

sizeof(int) = 4
sizeof(size_t) = 8
Data1: 200000 integers in random from -500 to 500 (many duplicated)
     Algo Name                   Time(s)
1    count                    0.0002865390
2    radix                    0.0063802410
3    btree                    0.0100811730
4    merge_r                  0.0127625810
5    merge                    0.0130818440
6    quick                    0.0144666640
7    heapify                  0.0145566040
8    shell                    0.0149387610
9    np.sort(numpy)           0.0159584780
10   qsort(glibc)             0.0162465800
11   shell2                   0.0187523920
12   list.sort(python)        0.0216216080
13   sorted(python)           0.0228952610
14   binsert2                 0.6138220350
15   binsert                  0.6154471680
16   insert2                  3.3854721020
17   insert                   4.6864306390
18   selects                  7.7486197970
19   bubble                   48.3289254720

Data2: 200000 integers in random from -2147483648 to 2147483647
     Algo Name                   Time(s)
1    quick                    0.0121813170
2    merge_r                  0.0154146260
3    merge                    0.0159740240
4    heapify                  0.0164701320
5    shell                    0.0185461380
6    qsort(glibc)             0.0195465400
7    radix                    0.0201735410
8    np.sort(numpy)           0.0210044280
9    shell2                   0.0234900200
10   btree                    0.0437949200
11   sorted(python)           0.0453653430
12   list.sort(python)        0.0466786440
13   binsert                  0.5995638920
14   binsert2                 0.6202496610
15   insert2                  3.3880157650
16   insert                   4.6766841610
17   selects                  7.7102677510
18   bubble                   48.3651019260
19   count                    E:3
```
