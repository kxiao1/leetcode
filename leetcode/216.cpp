// Subset sum-ish
// https://leetcode.com/problems/combination-sum-iii/description/
// List all choices of k numbers from 1-9 that sum to n
/* References:
https://walkccc.me/LeetCode/problems/216/ (DFS, no memoization)
Complexity is 9CK - we are enumerating all possible ways to choose k out of 9
Memoization is not used because we can't store only the 'tail' once the entire
vector has been generated

What about a 2^9 solution? See 416.py (O(nk) with top-down DP, but here we can't memoize)

In general, if we replace 9 with a variable we must refer to e.g.//
https://math.stackexchange.com/questions/2081091/counting-distinct-partition-sets-of-integer

Simpler question: generate all possible combinations of length k from characters
a-c with repeats. Then one solutions is [a, b, c] -> [[a, a], [b, a], [c, a]]
-> [[a, a], [b, a], [c, a], [a, b], [b, b], [c, b]]
-> [[a, a], [b, a], [c, a], [a, b], [b, b], [c, b], [a, c], [b, c], [c, c]]
... (go to the next loop iteration)

We have four tiers of counting
1) Repeats allowed, order matters (1D dp, top down - Hackerrank lego_blocks)
2) Repeats allowed, order does not matter (1D dp, bottom up - 518.py)
3) No repeats, no limit to no. of numbers used (classic knapsack - 2D dp)
4) No repeats, exact no. of numbers used (this problem, try out all 9Ck)
 
no. of combinations: bottom up
list of combinations: top down

*/
#include <vector>

// The solution here is similar to 518.py - bottom up
// Bottom up is actually less efficient if we don't want duplicates (unlike 518)
// In this case, the complexity depends on n(!!)
class Solution {
   public:
    std::vector<std::vector<int>> combinationSum3(int k, int n) {
        // For each sum, there is a vector of different possible combinations
        std::vector<std::vector<std::vector<int>>> grid(n + 1);
        grid[0].push_back(std::vector<int>());

        // start using 1's, then 2's...
        for (int i = 1; i < 10; ++i) {
            // add the current number to existing vectors: start from sum = n
            // and go down so we don't add the same number repeatedly
            for (int j = n - i; j >= 0; --j) {
                for (auto vec : grid[j]) {
                    vec.push_back(i);
                    grid[i + j].push_back(vec);
                }
            }
        }
        // Filter the combinations that sum to n, make sure they use k numbers
        std::vector<std::vector<int>> out;
        for (auto& vec : grid[n]) {
            if (vec.size() == k) {
                out.push_back(vec);
            }
        }
        return out;
    }
};