#include <vector>
#include <iostream>
#include "tree.h"

/* simple debugging utilities when working with vectors and trees */

void debug_print_vec(std::string name, std::vector<int> vec)
{
    std::cout << name << ": ";
    for (auto elem : vec)
    {
        std::cout << elem << " ";
    }
    std::cout << std::endl;
}

void debug_print_tree(Tree *root, int depth) {
    if (root->left != nullptr) {
        debug_print_tree(root->left, depth + 1);
    }
    std::cout << (root->item) << "(" << depth << ") ";
    if (root->right != nullptr) {
        debug_print_tree(root->right, depth + 1);
    }
}

void debug_print_tree_wrap(Tree *root) {
    debug_print_tree(root, 0);
    std::cout <<std::endl;
}