#include <stdio.h>
#include <assert.h>
#include "common.h"


int
min_int()
{
    assert(sizeof(int)==2 || sizeof(int)==4);
    return 0x8000 << (sizeof(int)*8-16);
}


int
max_int()
{
    return ~min_int();
}


/* for qsort in libc */
int
cmp_int(const int *keyval, const int *datum)
{
    if (*keyval > *datum) return 1;
    if (*keyval == *datum) return 0;
    return -1;  // *keyval < *datum
}

