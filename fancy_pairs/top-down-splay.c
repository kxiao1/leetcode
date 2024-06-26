/*
                An implementation of top-down splaying
                    D. Sleator <sleator@cs.cmu.edu>
    	                     March 1992

  "Splay trees", or "self-adjusting search trees" are a simple and
  efficient data structure for storing an ordered set.  The data
  structure consists of a binary tree, without parent pointers, and no
  additional fields.  It allows searching, insertion, deletion,
  deletemin, deletemax, splitting, joining, and many other operations,
  all with amortized logarithmic performance.  Since the trees adapt to
  the sequence of requests, their performance on real access patterns is
  typically even better.  Splay trees are described in a number of texts
  and papers [1,2,3,4,5].

  The code here is adapted from simple top-down splay, at the bottom of
  page 669 of [3].  It can be obtained via anonymous ftp from
  spade.pc.cs.cmu.edu in directory /usr/sleator/public.

  The chief modification here is that the splay operation works even if the
  item being splayed is not in the tree, and even if the tree root of the
  tree is NULL.  So the line:

                              t = splay(i, t);

  causes it to search for item with key i in the tree rooted at t.  If it's
  there, it is splayed to the root.  If it isn't there, then the node put
  at the root is the last one before NULL that would have been reached in a
  normal binary search for i.  (It's a neighbor of i in the tree.)  This
  allows many other operations to be easily implemented, as shown below.

  [1] "Fundamentals of data structures in C", Horowitz, Sahni,
       and Anderson-Freed, Computer Science Press, pp 542-547.
  [2] "Data Structures and Their Algorithms", Lewis and Denenberg,
       Harper Collins, 1991, pp 243-251.
  [3] "Self-adjusting Binary Search Trees" Sleator and Tarjan,
       JACM Volume 32, No 3, July 1985, pp 652-686.
  [4] "Data Structure and Algorithm Analysis", Mark Weiss,
       Benjamin Cummins, 1992, pp 119-130.
  [5] "Data Structures, Algorithms, and Performance", Derick Wood,
       Addison-Wesley, 1993, pp 367-375.

  The following code was written by Daniel Sleator, and is released
  in the public domain. 
  (Cosmetic changes were made by kxiao1 in 2023 for C++ compatibility.)
*/

#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <assert.h>
#include "tree.h" /* Defines the following struct */

// typedef struct tree_node Tree;
// struct tree_node {
//     Tree *left, *right;
//     int item;
// };

int size; /* number of nodes in the tree */
/* Not actually needed for any of the operations */

// count the number of elements in a tree rooted at t
int count(Tree *t) {
    if (t == NULL) {
        return 0;
    }
    return 1 + count(t->left) + count(t->right);
}

Tree* splay(int i, Tree* t)
{
    /* Simple top down splay, not requiring i to be in the tree t.  */
    /* What it does is described above.                             */
    Tree N, *l, *r, *y;
    if (t == NULL)
        return t;
    N.left = N.right = NULL;
    l = r = &N;

    for (;;) {
        if (i < t->item) {
            if (t->left == NULL)
                break;
            if (i < t->left->item) {
                y = t->left; /* rotate right */
                t->left = y->right;
                y->right = t;
                t = y;
                if (t->left == NULL)
                    break;
            }
            r->left = t; /* link right */
            r = t;
            t = t->left;
        } else if (i > t->item) {
            if (t->right == NULL)
                break;
            if (i > t->right->item) {
                y = t->right; /* rotate left */
                t->right = y->left;
                y->left = t;
                t = y;
                if (t->right == NULL)
                    break;
            }
            l->right = t; /* link left */
            l = t;
            t = t->right;
        } else {
            break;
        }
    }
    l->right = t->left; /* assemble */
    r->left = t->right;
    t->left = N.right;
    t->right = N.left;
    return t;
}

Tree* insertNode(int i, Tree* t)
{
    /* Insert i into the tree t, unless it's already there.    */
    /* Return a pointer to the resulting tree.                 */
    Tree* new;

    new = (Tree*)malloc(sizeof(Tree));
    if (new == NULL) {
        printf("Ran out of space\n");
        exit(1);
    }
    new->item = i;
    if (t == NULL) {
        new->left = new->right = NULL;
        size = 1;
        return new;
    }
    t = splay(i, t);
    if (i < t->item) {
        new->left = t->left;
        new->right = t;
        t->left = NULL;
        size++;
        return new;
    } else if (i > t->item) {
        new->right = t->right;
        new->left = t;
        t->right = NULL;
        size++;
        return new;
    } else { /* We get here if it's already in the tree */
        /* Don't add it again                      */
        free(new);
        return t;
    }
}

Tree* deleteNode(int i, Tree* t)
{
    /* Deletes i from the tree if it's there.               */
    /* Return a pointer to the resulting tree.              */
    Tree* x;
    if (t == NULL)
        return NULL;
    t = splay(i, t);
    if (i == t->item) { /* found it */
        if (t->left == NULL) {
            x = t->right;
        } else {
            x = splay(i, t->left);
            x->right = t->right;
        }
        size--;
        free(t);
        return x;
    }
    return t; /* It wasn't there */
}

Tree* countNodes(int i, Tree* t, int* cnt) {
    t = splay(i, t);
    if (i >= t->item) {
        /* if we found it (root = i), return #items left of root */
        /* even if root < i, the root is still the largest element <= i */
        *cnt = count(t->left) + 1;
    } else {
        /* if the root > i, i is only larger than everything left of root */
        *cnt = count(t->left);
    }
    return t;
}
