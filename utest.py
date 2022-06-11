import unittest
import os
import random
import socket
import threading
import ctypes
import subprocess
from common import shell


class test_common_c(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n# common.c:')
        print('sizeof(int) = ', ctypes.sizeof(ctypes.c_int))
        print('sizeof(size_t) = ', ctypes.sizeof(ctypes.c_size_t))
        print(shell('gcc -Wall -Wextra -fPIC -shared -std=c99'
                    ' -O3 common.c -o common.so'))
        cls.cm = ctypes.CDLL('./common.so')

    @classmethod
    def tearDownClass(cls):
        os.remove('common.so')

    def get_cm(self):
        return test_common_c.cm

    def setUp(self):
        self.size_int = ctypes.sizeof(ctypes.c_int)
        self.size_t = ctypes.sizeof(ctypes.c_size_t)

    def test_min_int(self):
        f = self.get_cm().min_int
        if self.size_int == 4:
            self.assertEqual(f(), int.from_bytes(b'\x80\x00\x00\x00',
                                                 'big', signed=True))
        if self.size_int == 2:
            self.assertEqual(f(), int.from_bytes(b'\x80\x00',
                                                 'big', signed=True))

    def test_max_int(self):
        f = self.get_cm().max_int
        if self.size_int == 4:
            self.assertEqual(f(), int.from_bytes(b'\x7F\xFF\xFF\xFF',
                                                 'big', signed=True))
        if self.size_int == 2:
            self.assertEqual(f(), int.from_bytes(b'\x7F\xFF',
                                                 'big', signed=True))

    def test_cmp_int(self):
        a02 = (9,8,7,6,5,4,3,2,1)
        ca02 = (ctypes.c_int*9)(*a02)
        dca02 = ctypes.byref(ca02)
        a03 = (22,-11,33,-5,44,12,-9,10,6,1,-1,9,3,7,-2,5,-4,0,8,2,-18)
        ca03 = (ctypes.c_int*len(a03))(*a03)
        dca03 = ctypes.byref(ca03)
        libc = ctypes.CDLL('libc.so.6')
        libc.qsort(dca02, len(a02), self.size_int,
                   self.get_cm().cmp_int)
        self.assertEqual(list(ca02), sorted(a02))
        libc.qsort(dca03, len(a03),  self.size_int,
                   self.get_cm().cmp_int)
        self.assertEqual(list(ca03), sorted(a03))
        dd = [-2139398188, -1298145759, -841243177, -377333222,
              -238985207, 24440992, 235889693, 318629958, 1230034595,
              1848189910]
        cdd = (ctypes.c_int*len(dd))(*dd)
        dcdd = ctypes.byref(cdd)
        libc.qsort(dcdd, len(cdd), self.size_int,
                   self.get_cm().cmp_int)
        self.assertEqual(list(cdd), sorted(dd))


class test_sort_c(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n# sort.c:')
        print('sizeof(int) = ', ctypes.sizeof(ctypes.c_int))
        print('sizeof(size_t) = ', ctypes.sizeof(ctypes.c_size_t))
        print(shell('gcc -Wall -Wextra -fPIC -shared -std=c99'
                    ' -O3 common.c sort.c -o sort.so'))
        cls.sort = ctypes.CDLL('./sort.so')

    @classmethod
    def tearDownClass(cls):
        os.remove('sort.so')

    def get_sort(self):
        return test_sort_c.sort

    def setUp(self):
        self.size_int = ctypes.sizeof(ctypes.c_int)
        self.size_t = ctypes.sizeof(ctypes.c_size_t)
        # here keep all int in 2 bytes range
        self.a01 = (1,2,3,4,5,6,7,8,9)
        self.ca01 = (ctypes.c_int*9)(*self.a01)
        self.dca01 = ctypes.byref(self.ca01)
        self.a02 = (9,8,7,6,5,4,3,2,1)
        self.ca02 = (ctypes.c_int*9)(*self.a02)
        self.dca02 = ctypes.byref(self.ca02)
        self.a03 = (22,-11,33,-5,44,12,-9,10,6,1,-1,9,3,7,-2,5,-4,0,8,2,-18)
        self.ca03 = (ctypes.c_int*len(self.a03))(*self.a03)
        self.dca03 = ctypes.byref(self.ca03)
        self.a04 = (1,1,1,1,1)
        self.ca04 = (ctypes.c_int*len(self.a04))(*self.a04)
        self.dca04 = ctypes.byref(self.ca04)
        self.a05 = []
        for i in range(8000):
            self.a05.append(random.randint(-5000,5000))
        self.ca05 = (ctypes.c_int*len(self.a05))(*self.a05)
        self.dca05 = ctypes.byref(self.ca05)
        self.a06 = (12345,1234)
        self.ca06 = (ctypes.c_int*len(self.a06))(*self.a06)
        self.dca06 = ctypes.byref(self.ca06)

    def tearDown(self):
        ...

    def test_get_radix(self):
        f = self.get_sort().get_radix
        self.assertEqual(f(123,0), 3)
        self.assertEqual(f(123,1), 2)
        self.assertEqual(f(123,2), 1)
        self.assertEqual(f(123,3), 0)
        self.assertEqual(f(123,4), 0)
        self.assertEqual(f(-123,0), 3)
        self.assertEqual(f(-123,1), 2)
        self.assertEqual(f(-123,2), 1)
        self.assertEqual(f(-123,3), 0)
        self.assertEqual(f(-123,4), 0)
        self.assertEqual(f(0,0), 0)
        self.assertEqual(f(0,4), 0)
        if self.size_int == 4:
            self.assertEqual(f(23456789,5), 4)
            self.assertEqual(f(-23456789,5), 4)

    def test_split_np(self):
        f = self.get_sort().split_np
        a = (1,2,-3,4,5,-6,7)
        ca = (ctypes.c_int*7)(*a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 7), 2)
        self.assertEqual(ca[0], -3)
        self.assertEqual(ca[1], -6)
        a = (-1,-2,-3,-4,-5,-6,-7)
        ca = (ctypes.c_int*7)(*a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 7), 7)
        a = (1,2,3,4,5,6,7)
        ca = (ctypes.c_int*7)(*a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 7), 0)
        a = (0)
        ca = (ctypes.c_int*1)(a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 1), 0)

    def test_get_max(self):
        f = self.get_sort().get_max
        a = (1,2,-3,4,5,-6,7)
        ca = (ctypes.c_int*7)(*a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 7), 7)
        self.assertEqual(f(dca, 1), 1)

    def test_get_min(self):
        f = self.get_sort().get_min
        a = (1,2,-3,4,5,-6,7)
        ca = (ctypes.c_int*7)(*a)
        dca = ctypes.byref(ca)
        self.assertEqual(f(dca, 7), -6)
        self.assertEqual(f(dca, 1), 1)

    def do_call(self, sort):
        sort(self.dca01, 9)
        self.assertEqual(tuple(self.ca01), self.a01)
        sort(self.dca02, 0)
        self.assertEqual(tuple(self.ca02), self.a02)
        sort(self.dca02, 9)
        self.assertEqual(tuple(self.ca02), self.a01)
        sort(self.dca03, len(self.a03))
        self.assertEqual(list(self.ca03), sorted(self.a03))
        sort(self.dca04, len(self.a04))
        self.assertEqual(list(self.ca04), sorted(self.a04))
        sort(self.dca04, len(self.a04)-2)
        self.assertEqual(list(self.ca04), sorted(self.a04))
        sort(self.dca05, len(self.a05))
        self.assertEqual(list(self.ca05), sorted(self.a05))
        sort(self.dca06, len(self.a06))
        self.assertEqual(list(self.ca06), sorted(self.a06))

    def test_bubble(self):
        self.do_call(self.get_sort().bubble)

    def test_selects(self):
        self.do_call(self.get_sort().selects)

    def test_insert(self):
        self.do_call(self.get_sort().insert)

    def test_insert2(self):
        self.do_call(self.get_sort().insert2)

    def test_binsert(self):
        self.do_call(self.get_sort().binsert)

    def test_binsert2(self):
        self.do_call(self.get_sort().binsert2)

    def test_shell(self):
        self.do_call(self.get_sort().shell)

    def test_shell2(self):
        self.do_call(self.get_sort().shell2)

    def test_merge(self):
        f = self.get_sort().merge
        self.do_call(f)
        d1 = [1,2]
        cd1 = (ctypes.c_int*2)(*d1)
        self.assertEqual(f(ctypes.byref(cd1),
                         int.from_bytes(b'\xff'*self.size_t,'big')), 1)

    def test_heapify(self):
        self.do_call(self.get_sort().heapify)

    def test_radix(self):
        self.do_call(self.get_sort().radix)

    def test_btree(self):
        self.do_call(self.get_sort().btree)

    def test_count(self):
        f = self.get_sort().count
        mlimit = 1024**3
        f(self.dca01, 9, mlimit)
        self.assertEqual(tuple(self.ca01), self.a01)
        f(self.dca02, 0, mlimit)
        self.assertEqual(tuple(self.ca02), self.a02)
        f(self.dca02, 9, mlimit)
        self.assertEqual(tuple(self.ca02), self.a01)
        f(self.dca03, len(self.a03), mlimit)
        self.assertEqual(list(self.ca03), sorted(self.a03))
        f(self.dca04, len(self.a04), mlimit)
        self.assertEqual(list(self.ca04), sorted(self.a04))
        f(self.dca04, len(self.a04)-2, mlimit)
        self.assertEqual(list(self.ca04), sorted(self.a04))
        f(self.dca05, len(self.a05), mlimit)
        self.assertEqual(list(self.ca05), sorted(self.a05))
        self.assertEqual(f(self.dca05,len(self.a05),0), 3)
        f(self.dca06, len(self.a06), mlimit)
        self.assertEqual(list(self.ca06), sorted(self.a06))
        #
        d2 = []
        for i in range(256):
            d2.append(1)
        cd2 = (ctypes.c_int*256)(*d2)
        self.assertEqual(f(ctypes.byref(cd2),256,mlimit), 2)
        d3 = []
        for i in range(255):
            d3.append(1)
        cd3 = (ctypes.c_int*255)(*d3)
        self.assertEqual(f(ctypes.byref(cd2),255,mlimit), 0)
        self.assertEqual(list(cd3),d3)
        if self.size_int == 4 and self.size_t== 8:
            d1 = [-2147483648,2147483647]
            cd1 = (ctypes.c_int*2)(*d1)
            self.assertEqual(f(ctypes.byref(cd1),2,mlimit), 3)
            mlimit2 = ctypes.c_size_t(4*1024**3)
            self.assertEqual(f(ctypes.byref(cd1),2,mlimit2), 0)
            self.assertEqual(list(cd1), d1)
        if self.size_int == 4 and self.size_t == 4:
            d1 = [-2147483648,2147483647]
            cd1 = (ctypes.c_int*2)(*d1)
            self.assertEqual(f(ctypes.byref(cd1),2,mlimit), 3)

    def do_call2(self, sort):
        sort(self.dca01, 0, 9-1)
        self.assertEqual(tuple(self.ca01), self.a01)
        sort(self.dca02, 0, 0)
        self.assertEqual(tuple(self.ca02), self.a02)
        sort(self.dca02, -1, 0)
        self.assertEqual(tuple(self.ca02), self.a02)
        sort(self.dca02, 0, 9-1)
        self.assertEqual(tuple(self.ca02), self.a01)
        sort(self.dca03, 0, len(self.a03)-1)
        self.assertEqual(list(self.ca03), sorted(self.a03))
        sort(self.dca04, 0, len(self.a04)-1)
        self.assertEqual(list(self.ca04), sorted(self.a04))
        sort(self.dca04, 0, len(self.a04)-3)
        self.assertEqual(list(self.ca04), sorted(self.a04))
        sort(self.dca05, 0, len(self.a05)-1)
        self.assertEqual(list(self.ca05), sorted(self.a05))
        sort(self.dca06, 0, 1)
        self.assertEqual(list(self.ca06), sorted(self.a06))

    def test_quick(self):
        self.do_call2(self.get_sort().quick)

    def test_merge_r(self):
        self.do_call2(self.get_sort().merge_r)


if __name__ == '__main__':
    unittest.main()

