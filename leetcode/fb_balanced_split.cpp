#include <span>
#include <random>
#include <vector>
#include <iostream>

class Rand_int {
public:
    Rand_int(int low, int high)
        : dist(low, high) {}
    double operator()() { return dist(re); } // draw an int
    void seed(int s) { re.seed(s); } // choose new random engine seed
private:
    std::default_random_engine re;
    std::uniform_real_distribution<> dist;
};

// Experimental C++20 solution
class Solution {
public:
    bool balancedSplit(std::vector<int>&& nums) {
        int s = std::reduce(nums.begin(), nums.end());
        if (s % 2 == 1) {
            return false;
        }

        // we want to find a left partition that sums to goal
        int goal = s / 2; // we know s / 2 is actually an integer
        Rand_int rnd { 0, 1 };

        std::span<int> nums_span(nums);
        while (s > goal) {
            int idx = rnd() * nums_span.size(); // round down to int
            int v = nums_span[idx]; // our pivot
            
            // we want three groups: [0, less), [less, greater), [greater, max)
            auto greater = std::partition(nums_span.begin(), nums_span.end(), 
                            [v](int x){ return x <= v;});
            auto less = std::partition(nums_span.begin(), greater,
                            [v](int x){ return x < v;});

            int rSum = std::reduce(greater, nums_span.end());
            int lSumPivot = s - rSum;

            if (lSumPivot > goal) { // case 1: recurse on left
                nums_span = std::span<int>(nums_span.begin(), less);
                
                // pivot goes right, need to move some elements from left to right
                int pivotSum = (greater - less) * v;
                s = lSumPivot - pivotSum; 
            } else { // case 2: recurse on right
                nums_span = std::span<int>(greater, nums_span.end());
                
                // pivot goes left, need to move some elements from right to left
                s = rSum;
                goal -= lSumPivot; 
            }
        }

        return goal == s;
    }
};

// output: 1,0,1,0,0,1,0,0,1
int main() {
    Solution s;
    std::cout << s.balancedSplit({1,5,7,1}) << std::endl;
    std::cout << s.balancedSplit({12,7,6,7,6}) << std::endl;
    std::cout << s.balancedSplit({}) << std::endl;
    std::cout << s.balancedSplit({2}) << std::endl;
    std::cout << s.balancedSplit({20,2}) << std::endl;
    std::cout << s.balancedSplit({5,7,20,12,5,7,6,14,5,5,6}) << std::endl;
    std::cout << s.balancedSplit({5,7,20,12,5,7,6,7,14,5,5,6}) << std::endl;
    std::cout << s.balancedSplit({1,1,1,1,1,1,1,1,1,1,1,1}) << std::endl;
    std::cout << s.balancedSplit({0,0,0}) << std::endl;
    
    return 0;
}