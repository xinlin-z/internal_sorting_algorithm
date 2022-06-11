/* sorting algorithms for int array */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "common.h"
#include "sort.h"


/* a^=b^=a^=b version is not safe enough,
 * if they point to the same address, so use safe and stupid version.
 * And it's also a no warning, and more readable version. */
static inline void
swap(int *a, int *b)
{
    int t;

    t = *a;
    *a = *b;
    *b = t;
}


void
bubble(int a[], size_t n)
{
    if (n > 1) {
        size_t i,j;

        for (i=0; i<n-1; ++i) {
            for (j=0; j<n-i-1; ++j) {
                if (a[j] > a[j+1]) swap(a+j, a+j+1);
            }
        }
    }
}


void
selects(int a[], size_t n)  // conflict name of select, so selects
{
    size_t i,j,k;

    for (i=n; i>1; --i) {
        k = 0;
        for (j=1; j<i; ++j)
            if (a[k] < a[j]) k = j;
        if (k != j-1) swap(a+k, a+j-1);
    }
}


/* If data is linked in memory by pointer, by using insert algorithm,
 * there is no need to move elements. We could directly modify the
 * pointers to complete the insert action. That would be more efficient.
 * Below is an implementation of the idea of insert on int array. */
void
insert(int a[], size_t n)
{
    int t;
    size_t i,j;

    for (i=1; i<n; ++i) {
        t = a[i];
        for (j=i; j>0&&a[j-1]>t; --j);
        memmove(a+j+1, a+j, sizeof(int)*(i-j));  // cannot be memcpy
        a[j] = t;
    }
}


void
insert2(int a[], size_t n)
{
    int t;
    size_t i,j;

    for (i=1; i<n; ++i) {
        t = a[i];
        for (j=i; j>0; --j)
            if (a[j-1] > t) a[j] = a[j-1];
            else break;
        a[j] = t;
    }
}


/* binary insert */
void
binsert(int a[], size_t n)
{
    int t;
    size_t i,j,low,mid,high;

    for (i=1; i<n; ++i) {
        t = a[i];
        /* binary search */
        low = 0;
        high = i-1;
        while (low < high) {
            mid = (low+high) / 2;
            if (a[mid] > t) high = mid;
            else low = mid + 1;
        }
        /* here we get low == high */
        if (a[low] > t) j = low;
        if (a[low] <= t) j = low + 1;
        if (j == i) continue;
        memmove(a+j+1, a+j, sizeof(int)*(i-j));
        a[j] = t;
    }
}


void
binsert2(int a[], size_t n)
{
    int t;
    size_t i,j,k,low,mid,high;

    for (i=1; i<n; ++i) {
        t = a[i];
        /* binary search */
        low = 0;
        high = i-1;
        while (low < high) {
            mid = (low+high) / 2;
            if (a[mid] > t) high = mid;
            else low = mid + 1;
        }
        /* here we get low == high */
        if (a[low] > t) j = low;
        if (a[low] <= t) j = low + 1;
        if (j == i) continue;
        k = i;
        while (k != j) {
            a[k] = a[k-1];
            k--;
        }
        a[j] = t;
    }
}


void
shell(int a[], size_t n)
{
    int t;
    size_t i,j,k,u;

    for (i=n/2; i>0; i/=2) {          // define distance
        for (j=0; j<i; ++j) {         // rounds of insert
            for (k=i+j; k<n; k+=i) {  // single insert
                t = a[k];
                for (u=k; u>=i; u-=i) {
                    if (a[u-i] > t)
                        a[u] = a[u-i];
                    else break;
                }
                a[u] = t;
            }
        }
    }
}


void
shell2(int a[], size_t n)
{
    int t;
    size_t i,j,k,u;

    for (i=n/2; i>0; i/=2) {          // define distance
        if (i == 1)
            binsert(a, n);
        else {
            for (j=0; j<i; ++j) {         // rounds of insert
                for (k=i+j; k<n; k+=i) {  // single insert
                    t = a[k];
                    for (u=k; u>=i; u-=i) {
                        if (a[u-i] > t)
                            a[u] = a[u-i];
                        else break;
                    }
                    a[u] = t;
                }
            }
        }
    }
}


int
merge(int a[], size_t n)
{
    if (n > 1) {
        size_t i,j,k,s,hs,m;

        /* use malloc, in case the size is bigger than stack */
        int *t = (int*)malloc(sizeof(int)*n);
        if (t == NULL) return 1;

        for (s=2; s<n*2; s*=2) {
            hs = s/2;
            m = 0;
            for (i=0; i<n; i+=s) {
                j = i;
                k = i + hs;
                while (m<i+s && m<n) {
                    if (k>=n && j<n) {
                        t[m++] = a[j++]; continue;
                    }
                    if (j==i+hs && k<i+s) {
                        t[m++] = a[k++]; continue;
                    }
                    if (k==i+s && j<i+hs) {
                        t[m++] = a[j++]; continue;
                    }
                    if (a[j] < a[k]) t[m++] = a[j++];
                    else t[m++] = a[k++];
                }
            }
            memcpy(a, t, sizeof(int)*n);
        }
        free(t);
    }
    return 0;
}


/* Maybe it's worth to think about the Stack Length when data number
 * is too big and to use recursive algorithms. */


static void
_merge(int a[], int *t, size_t li, size_t m, size_t ri)
{
    size_t i = li;
    size_t j = m+1;
    size_t k = 0;
    size_t len = ri - li + 1;

    while (k < len) {
        if (i == m+1) {
            t[k++] = a[j++]; continue;
        }
        if (j == ri+1) {
            t[k++] = a[i++]; continue;
        }
        if (a[i] < a[j]) t[k++] = a[i++];
        else t[k++] = a[j++];
    }
    memcpy(a+li, t, sizeof(int)*len);
}


void
_merge_r(int a[], int *t, size_t li, size_t ri)
{
    if (li < ri) {
        size_t m = (li+ri)/2;
        _merge_r(a, t, li, m);
        _merge_r(a, t, m+1, ri);
        _merge(a, t, li, m, ri);
    }
}


/* merge sort, recursive version */
int
merge_r(int a[], size_t li, size_t ri)
{
    if (li < ri) {
        int *t = (int*)malloc(sizeof(int)*(ri-li+1));
        if (t == NULL) return 1;
        _merge_r(a, t, li, ri);
        free(t);
    }
    return 0;
}


void
quick(int a[], size_t li, size_t ri)
{
    if (li >= ri) return;
    size_t i,p;

    p = li;
    for (i=li+1; i<=ri; ++i) {
        if (a[li] > a[i])
            if (++p != i) swap(a+p, a+i);
    }

    swap(a+li, a+p);
    quick(a, li, p);  // p-1 may be too big in case of overflow.
    quick(a, p+1, ri);
}


/* The Complete Binary Tree has a very import feature:
 * if i is index+1, which means index starts from one, not zero,
 * a[2i] is the left node of a[i], a[2i+1] is just the right node,
 * so, a[i/2] is always the parent of a[i],
 * so, if there are n nodes, a[n/2] is the first node which has leaves. */


/* Adjust heap, assuming from a[s+1] to a[e] is already an adjusted heap.
 * We only need to find the right place for a[s]. */
static void
_heap_adjust(int a[], size_t s, size_t e)  // s and e are index+1
{
    size_t i;

    for (i=s*2; i<=e; i*=2) {
        if (i+1<=e && a[i-1]<a[i]) ++i;  // find the bigger child
        if (a[s-1] < a[i-1]) {
            swap(a+s-1, a+i-1);
            s = i;
        }
        else break;
    }
}


void
heapify(int a[], size_t n)
{
    if (n > 1) {
        size_t i;

        /* create big heap  */
        for (i=n/2; i>0; --i) {
            _heap_adjust(a, i, n);
        }

        /* sorting */
        for (i=n; i>1; --i) {
            swap(a, a+i-1);
            _heap_adjust(a, 1, i-1);
        }
    }
}


typedef struct btree_node {
    int val;
    size_t count;
    struct btree_node *left;
    struct btree_node *right;
} BTNODE;


static BTNODE *
insert_tree(BTNODE *root, int a, BTNODE *node)
{
    if (root == NULL) {
        node->left = node->right = NULL;
        node->val = a;
        node->count = 1;
        root = node;
    }
    else if (a < root->val) {
        root->left = insert_tree(root->left, a, node);
    }
    else if (a == root->val) {
        root->count++;
    }
    else if (a > root->val) {
        root->right = insert_tree(root->right, a, node);
    }
    return root;
}


static void
walk_tree(int a[], BTNODE *root, size_t *i)
{
    if (root != NULL) {
        walk_tree(a, root->left, i);
        while (root->count--)
            a[(*i)++] = root->val;
        walk_tree(a, root->right, i);
    }
}


int
btree(int a[], size_t n)
{
    if (n > 1) {
        BTNODE *bmem = (BTNODE*)malloc(sizeof(BTNODE)*n);
        if (bmem == NULL) return 1;
        size_t *mi = (size_t*)malloc(sizeof(size_t));
        if (mi == NULL) {
            free(bmem);
            return 1;
        }
        BTNODE *root = NULL;

        for (size_t i=0; i<n; ++i)
            root = insert_tree(root, a[i], bmem+i);

        *mi = 0;
        walk_tree(a, root, mi);
        free(bmem);
    }
    return 0;
} 


/* Both radix and count are based on bucket sort idea!  */
typedef struct intdata {
    int val;
    struct intdata *link;  // to next
} INTD;


typedef struct {
    UINT radix;
    INTD *head;
    INTD *tail;
} RADIX;


/* radix is just like base */
UINT
get_radix(int a, UINT order)
{
    a = abs(a);
    for (UINT i=0; i<order; ++i) a /= 10;
    return a%10;
}


/* pos: boundary between negative and positive int,
 * pos is the first positive int position. */
size_t
split_np(int a[], size_t n)
{
    size_t pos=0,i;

    while (a[pos]<0 && pos<n) ++pos;
    if (pos != n) {
        for (i=pos+1; i<n; ++i)
            if (a[i] < 0) {
                swap(a+i, a+pos++);
            }
    }
    return pos;
}


static int
distribute(int a[], RADIX radix[], INTD *ad, size_t si, size_t n, UINT order)
{
    size_t i,j,k=0;
    INTD *t;

    for (i=si; i<n; ++i) {
        j = get_radix(a[i], order);
        if (j != 0) k=1;
        t = ad + i - si;
        t->val = a[i];
        t->link = NULL;
        if (radix[j].head == NULL) {
            radix[j].head = t;
            radix[j].tail = t;
        }
        else {
            radix[j].tail->link = t;
            radix[j].tail = t;
        }
    }
    return k;
}


static void
collect(int a[], RADIX radix[], size_t si, int ascend)
{
    size_t i,j=si;
    INTD *t;
    UINT b[] = {0,1,2,3,4,5,6,7,8,9};

    if (ascend == 0)
        for (i=0; i<10; ++i) b[i] = 9-i;

    for (i=0; i<10; ++i) {
        while (radix[b[i]].head != NULL) {
            t = radix[b[i]].head;
            radix[b[i]].head = radix[b[i]].head->link;
            a[j++] = t->val;
        }
    }
}


int
radix(int a[], size_t n)
{
    if (n > 1) {
        UINT k,order;
        RADIX radix[] = {
                    {0, NULL, NULL},
                    {1, NULL, NULL},
                    {2, NULL, NULL},
                    {3, NULL, NULL},
                    {4, NULL, NULL},
                    {5, NULL, NULL},
                    {6, NULL, NULL},
                    {7, NULL, NULL},
                    {8, NULL, NULL},
                    {9, NULL, NULL},
              };
        /* first of all, try to get enough memory */
        INTD *ad = (INTD*)malloc(sizeof(INTD)*n);
        if (ad == NULL) return 1;

        const size_t pos = split_np(a, n);
        /* negative part */
        if (pos != 0) {
            order = 0;
            do {
                k = distribute(a, radix, ad, 0, pos, order++);
                collect(a, radix, 0, 0);
            } while (k);
        }

        /* positive part */
        if (pos != n) {
            order = 0;
            do {
                k = distribute(a, radix, ad, pos, n, order++);
                collect(a, radix, pos, 1);
            } while (k);
        }

        free(ad);
    }
    return 0;
}


int
get_max(int a[], size_t n)
{
    assert(n != 0);
    int t = a[0];
    for (size_t i=1; i<n; ++i)
        if (t < a[i]) t = a[i];
    return t;
}


int
get_min(int a[], size_t n)
{
    assert(n != 0);
    int t = a[0];
    for (size_t i=1; i<n; ++i)
        if (t > a[i]) t = a[i];
    return t;
}


int
count(int a[], size_t n, size_t mem_limit)
{
    if (n > 1) {
        if (mem_limit == 0) return 3;
        size_t i,j=0;
        int m = get_min(a, n);
        int k = get_max(a, n);
        size_t mlen = k-m+1;
        if (mlen == 0) {  // int overflow
            if (sizeof(size_t) > sizeof(int))
                mlen = ((size_t)max_int()+1)*2;  // int size
            else if (sizeof(size_t) == sizeof(int))
                mlen = -1;  // biggest size_t
            else assert(0);
        }
        /* memory limit check  */
        if (mlen > mem_limit) return 3;
        /* start malloc */
        UINT8 *counter = (UINT8*)malloc(mlen);
        if (counter == NULL) return 1;  // OOM
        memset(counter, 0, mlen);
        /* count */
        for (i=0; i<n; ++i) {
            if (counter[a[i]-m] == 255) {
                free(counter);
                return 2;  // too man duplicated
            }
            counter[a[i]-m]++;
        }
        /* sort */
        for (i=0; i<mlen; ++i)
            while (counter[i]--) a[j++] = i + m;
        free(counter);
    }
    return 0;
}


//int main()
//{
//    int a1[] = {1,1,1,1,2,3,3,3,3,3,3,3,3,4,5};
//    bubble(a1, 15);
//    for (int i=0; i<15; ++i) {
//        printf("%d ", a1[i]);
//    }
//    printf("\n");
//
//    /*int a[] = {22,-11,33,-5,44,12,-9,10,6,1,-1,9,3,7,-2,5,-4,0,8,2,-18};
//    count(a, 21);
//    for (int i=0; i<21; ++i) {
//        printf("%d ", a[i]);
//    }
//    printf("\n");
//
//    printf("a test of 0x8000<<0 -> 0x%x\n", 0x8000<<0);
//    printf("min int = %d\n", min_int());
//    printf("max int = %d\n", max_int());
//    size_t tt = -1;
//    printf(".. %lu ..\n", tt);*/
//}


