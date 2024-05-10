#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

/*
    You start with three stacks h1-h3 of blocks. What is the maximum height at
   which the stacks are made equal by removing blocks?
*/

int equalStacks(std::vector<int>& h1, std::vector<int>& h2,
                std::vector<int>& h3) {
    std::vector<std::vector<int>> vs;
    std::vector<int> ss;
    for (const auto& v : {h1, h2, h3}) {
        vs.push_back(std::vector<int>(v.rbegin(), v.rend()));
        ss.push_back(std::reduce(v.begin(), v.end()));
    }
    std::vector<int> idxs{0, 1, 2};

    // while (side-effect expr, bool), where side-effect expr can be an
    // assignment but not a declaration, otherwise the compiler thinks the part
    // after the comma is another declaration (if (decl; bool) is ok from c++17)
    int max_idx;
    while (max_idx = *std::max_element(
               idxs.begin(), idxs.end(),
               [&](int i1, int i2) { return ss[i1] < ss[i2]; }),
           ss[max_idx] > *std::min_element(ss.begin(), ss.end())) {
        auto& v{vs[max_idx]};
        ss[max_idx] -= v.back();
        v.pop_back();
    }
    return ss[0];
}

int main() {
    int a, b;
    std::cin >> a >> b;  // type into keyboard, or echo and pipe
    std::cout << a << b;
}