#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

#include "assert.h"
#include "tree.h"  // a balanced binary search tree

/*
  Given a positve array vx of x1 x2 ... xn, and a positive array vy of y1 y2
  ...yn, a fancy pair 1 <= (i,j) <= n is where 0 < xi + xj <= k1, and 0 < yi +
  yj <= k2. The function fancy_pairs should return the number of (unordered)
  fancy pairs (i,j). xi's are distinct and yi's are distinct.

  Idea: Iterate backwards through the (xi,yi) pairs sorted by x, and maintain an
  increasing list of x prefixes that satisfy the k1 criteria. During the same
  pass, add yi's corresponding to the valid x prefixes to a bst and count how
  many satisfy k2 with the current y in the backward iteration (this is our
  index j). For every valid pair (i,j), we will pass by j first then i so we
  count it twice. Furthermore we will have accidentally included (i,i), so we
  need to subtract that also. These nuances are handled below.

  This solution is the "first pass" based on Zack's algorithm, so it is not very
  clean. The emphasis is on using explicit tree operations, and in the end
  Sleator's C splay tree code was used with external linkage (although we could
  well have used std::map instead, hence see the new solution too). To compile
  it, we have to go through makefiles.

  Compile this code with:
  make -f makeFancyPairs fancy_pairs.out

*/

int fancy_pairs(std::vector<int> vx, std::vector<int> vy, int k1, int k2) {
    assert((vx.size() == vy.size()) && (vx.size() >= 2));

    // sort vx and vy both on x
    std::vector<std::pair<int, int>> pairs;
    for (size_t i = 0; i < vx.size(); ++i) {
        pairs.push_back(std::make_pair(vx[i], vy[i]));
    }
    std::sort(pairs.begin(),
              pairs.end());  // by default we sort on the first element
    for (size_t i = 0; i < pairs.size(); ++i) {
        // replace the elements in vx and vy with the sorted lists
        vx[i] = pairs[i].first;
        vy[i] = pairs[i].second;
    }

    Tree* bst = nullptr;
    int count = 0;
    // Iterate in decreasing x order
    size_t maxX = 0;
    for (size_t i = vx.size(); i > 0; --i) {
        int allowanceX = k1 - vx[i - 1];
        if (vx[maxX] > allowanceX) {
            continue;
        }

        // find the largest j < i such that x_j <= allowance
        while (vx[maxX] <= allowanceX) {
            bst = insertNode(vy[maxX], bst);
            ++maxX;
        }
        --maxX;

        // remove the current vy element from the tree, to prevent self-matches
        // we can avoid this delete-insert operation pair by manually
        // calculating if a self-match will occur, and subtracting from the
        // count if so
        if (maxX >= i - 1) {
            bst = deleteNode(vy[i - 1], bst);
        }

        // at this point, every y_j in bst is fair game
        int allowanceY = k2 - vy[i - 1];
        int newCount;
        bst = countNodes(allowanceY, bst, &newCount);
        count += newCount;

        // put the removed element back
        if (maxX >= i - 1) {
            bst = insertNode(vy[i - 1], bst);
        }

    }

    // Account for the double count
    return count / 2;
}

int fancy_pairs_naive(std::vector<int> vx, std::vector<int> vy, int k1,
                      int k2) {
    assert((vx.size() == vy.size()) && (vx.size() >= 2));
    int count = 0;
    for (size_t i = 0; i < vx.size(); ++i) {
        for (size_t j = i + 1; j < vy.size(); ++j) {
            if ((vx[i] + vx[j] <= k1) && (vy[i] + vy[j] <= k2)) {
                ++count;
            }
        }
    }
    return count;
}

/* Turns out we didn't need a binary search for this problem. Ah well. */
// Run a binary search for the key k within index [0,max] of sorted vector v,
// returning the index of k or the largest element smaller than k (-1 if k is
// smaller than all elemnts)
int binarySearch(const std::vector<int>& v, int k, int max) {
    int low = 0;
    int high = max;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (v[mid] == k) {
            return mid;
        } else if (v[mid] >= k) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    // nothing found: low = high + 1 and k is between v[high] and v[low]
    return low - 1;
}

int main() {
    int size;
    std::cin >> size;

    // make a random permutation of [1, size]
    std::vector<int> domain(size);
    std::iota(domain.begin(), domain.end(), 1);
    std::random_shuffle(domain.begin(), domain.end());

    // pick the first 0.3 * size as x_i's, last 0.3 * size as y_i's
    std::vector<int> vx(domain.begin(), domain.begin() + 0.3 * size);
    std::vector<int> vy(domain.end() - 0.3 * size, domain.end());
    std::cout << "Using " << vx.size() << " different elements for vx and "
              << vy.size() << " different elements for vy" << std::endl;
    int k1 = 0.7 * size, k2 = 0.7 * size;

    int res_naive = fancy_pairs_naive(vx, vy, k1, k2);
    std::cout << "Naive algorithm: " << res_naive << std::endl;

    int res = fancy_pairs(vx, vy, k1, k2);
    std::cout << "Fast algorithm: " << res << std::endl;
}