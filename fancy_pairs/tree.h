// #pragma once // use this if tree.h gets included more than once
#ifdef __cplusplus
extern "C" {
#endif

// generic balanced binary search tree whose elements are ints
// NOTE: the tree will not maintain duplicates
typedef struct tree_node Tree;
struct tree_node {
    Tree *left, *right;
    int item;
};

Tree* insertNode(int i, Tree* t);
Tree* deleteNode(int i, Tree* t);

// Stores in *cnt # of elements in t <= i, and returns possibly reshaped t
Tree* countNodes(int i, Tree* t, int* cnt);

#ifdef __cplusplus
}
#endif