#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <vector>
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

  This solution tries to be terse and use modern C++.

  Compile this code with:
    g20 fancy_pairs_new.cpp -o fancy_pairs.o
  where g20 is aliased to g++10 -Wall -O2 -std=c++2a
*/

int fancy_pairs(std::vector<int> vx, std::vector<int> vy, int k1, int k2) {
    assert((vx.size() == vy.size()) && (vx.size() >= 2));
    int size = vx.size();
    std::vector<int> args(size);
    std::iota(args.begin(), args.end(), 0);
    std::sort(args.begin(), args.end(),  // argsort on x, biggest first
              [&vx](int i1, int i2) { return vx[i1] > vx[i2]; });

    std::vector<std::pair<int, int>> pairs(size);
    std::transform(  // if we write to vx, we need to pass vx by value to avoid
        args.begin(), args.end(), pairs.begin(),  // reading overwritten idxes
        [&vx, &vy](int idx) { return std::make_pair(vx[idx], vy[idx]); });

    int count{0};
    auto max_it{pairs.rbegin()};  // iterate backward to check against rbegin
    std::set<int> y_tree;
    for (auto [curr_x, curr_y] : pairs) {  // range-for from the biggest
        for (; max_it != pairs.rend() && (max_it->first + curr_x) <= k1;
             ++max_it) {
            y_tree.insert(max_it->second);  // same as emplace here
        }

        // std::distance is linear but this can be log if we store node sizes
        count += std::distance(y_tree.begin(), y_tree.upper_bound(k2 - curr_y));
        if (2 * curr_x <= k1 && 2 * curr_y <= k2) {
            --count;
        }
    }

    // Account for the double count
    return count / 2;
}

// Another solution that avoids double counting completely by preventing the
// start and end pointers from overlapping
int fancy_pairs2(std::vector<int> vx, std::vector<int> vy, int k1, int k2) {
    assert((vx.size() == vy.size()) && (vx.size() >= 2));
    std::vector<std::pair<int, int>> pairs(vx.size());
    std::transform(vx.begin(), vx.end(), vy.begin(), pairs.begin(),
                   [](int x, int y) { return std::make_pair(x, y); });
    std::sort(pairs.begin(), pairs.end(),
              [](auto& p1, auto& p2) { return p1.first > p2.first; });

    int count{0};
    auto max_it{
        std::prev(pairs.end())};  // iterate forward to check against end
    std::set<int> y_tree;
    for (auto [curr_x, curr_y] : pairs) {  // range-for from the biggest
        for (; max_it->first < curr_x && (max_it->first + curr_x) <= k1;
             --max_it) {
            y_tree.insert(max_it->second);  // same as emplace here
        }
        for (; max_it != pairs.end() && max_it->first >= curr_x; ++max_it) {
            y_tree.erase(max_it->second);  // if i >= j, force i < j
        }

        // std::distance is linear but this can be log if we store node sizes
        count += std::distance(y_tree.begin(), y_tree.upper_bound(k2 - curr_y));
    }

    return count;
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
    std::cout << "Fast algorithm1: " << res << std::endl;

    int res2 = fancy_pairs2(vx, vy, k1, k2);
    std::cout << "Fast algorithm2: " << res2 << std::endl;
}