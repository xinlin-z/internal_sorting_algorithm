#ifndef __SORT_H__
#define __SORT_H__


/* thread-safe sorting algorithms for int array */
void bubble(int a[], size_t n);
void selects(int a[], size_t n);
void insert(int a[], size_t n);
void insert2(int a[], size_t n);
void binsert(int a[], size_t n);
void binsert2(int a[], size_t n);
void shell(int a[], size_t n);
void shell(int a[], size_t n);
void heapify(int a[], size_t n);
void quick(int a[], size_t li, size_t ri);
int merge(int a[], size_t n);
int merge_r(int a[], size_t li, size_t ri);
int radix(int a[], size_t n);
int btree(int a[], size_t n);
int count(int a[], size_t n, size_t mem_limit);


#endif
