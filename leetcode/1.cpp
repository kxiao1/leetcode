// https://leetcode.com/problems/two-sum/description/
#include <unordered_map>
#include <vector>

class Solution {
   public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> vals;
        for (int i = 0; i < nums.size(); ++i) {
            if (auto it = vals.find(target - nums[i]); it != vals.end()) {
                return {i, it->second};
            }
            vals.insert_or_assign(nums[i], i);
        }
        return {};
    }

    // Assume the input array is sorted:
    // https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
    std::vector<int> twoSumSorted(std::vector<int>& numbers, int target) {
        int start{0}, end{(int)numbers.size() - 1};
        while (start < end) {
            int s = numbers[start] + numbers[end];
            if (s == target) {
                break;
            }
            if (s > target) {
                --end;
            } else {
                ++start;
            }
        }
        return {start + 1, end + 1};
    }

    // Suppose we want to find 3 numbers in the vector such that a + b = c (or
    // a^2 + b^2 = c^2, whatever), we have an O(n^2) solution of first fixing 
    // the target and then using either algorithm above
};