#include <algorithm>
#include <deque>
#include <iostream>
#include <numeric>
#include <ranges>
#include <vector>

// https://www.hackerrank.com/challenges/deque-stl/problem
// Keep the deque compact by storing indices to the original array
void printKMax(int arr[], int n, int k) {
    // Write your code here.
    std::deque<int> dq(k);
    std::iota(dq.begin(), dq.end(), 0);
    std::sort(dq.begin(), dq.end(),
              [&arr](int i, int j) { return arr[i] > arr[j]; });
    std::cout << arr[dq.front()] << " ";
    for (int idx = k; idx < n; ++idx) {
        while ((!dq.empty()) && dq.front() <= idx - k) {
            dq.pop_front();
        }
        while ((!dq.empty()) && arr[dq.back()] < arr[idx]) {
            dq.pop_back();
        }
        dq.push_back(idx);
        std::cout << arr[dq.front()] << " ";
    }
    std::cout << std::endl;
}

// Min of the sliding window maximums, for each window size in queries
// Gets rid of the iota and sorting...
std::vector<int> solve(std::vector<int> arr, std::vector<int> queries) {
    std::vector<int> out;
    for (int n : queries) {
        std::deque<int> window;
        int curr_min{1000000};
        for (int curr_idx = 0; curr_idx < (int)arr.size(); ++curr_idx) {
            while ((!window.empty()) && window.front() <= curr_idx - n) {
                window.pop_front();
            }
            while ((!window.empty()) && arr[window.back()] < arr[curr_idx]) {
                window.pop_back();
            }
            window.push_back(curr_idx);
            if (curr_idx >= n - 1) {
                curr_min = std::min(arr[window.front()], curr_min);
            }
        }
        out.push_back(curr_min);
    }
    return out;
}

int main() {
    std::vector<int> arr{
        176641, 818878, 590130, 846132, 359913, 699520, 974627, 806346, 343832,
        619769, 760242, 693331, 832192, 775549, 353117, 23950,  496548, 183204,
        971799, 393071, 727476, 351337, 811496, 24595,  417701, 664960, 745806,
        538176, 230403, 942316, 21481,  605695, 598531, 651683, 558460, 583357,
        530911, 721611, 308228, 724620, 429167, 909353, 330152, 116815, 986067,
        713467, 906132, 428600, 927889, 567272, 647109, 992614, 747948, 192884,
        879696, 262543, 782487, 829272, 470060, 427956, 751730, 597177, 870616,
        754791, 421830, 11676,  425656, 841955, 693419, 462693, 245403, 192649,
        750201, 180732, 17450,  44723,  527618, 174579, 515786, 444844, 210843,
        563425, 809540, 752036, 608529, 748313, 667439, 255643, 387412, 320353,
        704213, 755272, 267902, 657989, 651762, 325654, 582887, 382501, 715426,
        897450};
    std::vector<int> n{
        78, 96, 89, 29, 81, 17, 50, 34, 8,  17,  58, 7,  65, 59, 3,  58, 80,
        31, 21, 12, 87, 19, 6,  70, 60, 98, 55,  27, 67, 94, 57, 69, 14, 66,
        52, 73, 62, 73, 30, 77, 38, 23, 15, 63,  25, 72, 89, 91, 25, 38, 88,
        22, 48, 79, 71, 33, 72, 21, 26, 59, 100, 43, 77, 81, 55, 44, 43, 2,
        42, 48, 1,  30, 33, 71, 94, 58, 34, 93,  58, 27, 92, 91, 83, 47, 61,
        34, 25, 88, 37, 90, 3,  95, 5,  68, 39,  40, 71, 56, 89, 4};
    std::vector<int> res = solve(arr, n);
    std::vector<int> sol{
        992614, 992614, 992614, 809540, 992614, 809540, 986067, 841955, 527618,
        809540, 992614, 527618, 992614, 992614, 180732, 992614, 992614, 809540,
        809540, 750201, 992614, 809540, 527618, 992614, 992614, 992614, 992614,
        809540, 992614, 992614, 992614, 992614, 750201, 992614, 992614, 992614,
        992614, 992614, 809540, 992614, 870616, 809540, 755272, 992614, 809540,
        992614, 992614, 992614, 809540, 870616, 992614, 809540, 897450, 992614,
        992614, 841955, 992614, 809540, 809540, 992614, 992614, 870616, 992614,
        992614, 992614, 870616, 870616, 44723,  870616, 897450, 11676,  809540,
        841955, 992614, 992614, 992614, 841955, 992614, 992614, 809540, 992614,
        992614, 992614, 879696, 992614, 841955, 809540, 992614, 870616, 992614,
        180732, 992614, 527618, 992614, 870616, 870616, 992614, 992614, 992614,
        496548};
    std::cout << std::boolalpha << std::ranges::equal(res, sol) << "\n";
}
