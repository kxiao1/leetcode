#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

typedef std::pair<int, int> p;
bool comparator(const p& l, const p& r) { return l.first < r.first; }

// Find the maximum total volume without overlaps
// Dynamic Programming - Knapsack
int phoneCalls(vector<int> start, vector<int> duration, vector<int> volume) {
    vector<p> n(start.size());
    vector<int> ends(start.size());
    for (size_t i = 0; i < start.size(); ++i) {
        ends[i] = start[i] + duration[i];
        n[i] = p(ends[i], i);
    }

    // sort by end times
    sort(n.begin(), n.end(), comparator);
    vector<int> order(start.size());
    for (size_t i = 0; i < start.size(); ++i) {
        order[i] = n[i].second;
    }

    // make memo table
    vector<int> memo(start.size());

    for (size_t i = 0; i < start.size(); ++i) {
        int ord = order[i];
        int startT = start[ord];
        int val = volume[ord];
        int prevOrd = i;
        // find all tasks whose end times come before this startT
        while (prevOrd >= 0 && ends[order[prevOrd]] > startT) {
            --prevOrd;
        }
        int maxPrev = 0;
        if (prevOrd >= 0) {
            maxPrev =
                *max_element(memo.begin(), next(memo.begin(), prevOrd + 1));
        }
        memo[i] = maxPrev + val;
    }

    return *max_element(memo.begin(), memo.end());
}

int phoneCalls2(std::vector<int> start, std::vector<int> duration,
                std::vector<int> volume) {
    size_t n{start.size()};
    std::vector<std::pair<int, int>> intervals(n);
    std::transform(start.begin(), start.end(), duration.begin(),
                   intervals.begin(),
                   [](int s, int d) { return std::make_pair(s, s + d); });
    std::vector<std::pair<int, int>> end_volumes(n);
    std::transform(
        intervals.begin(), intervals.end(), volume.begin(), end_volumes.begin(),
        [](const auto& p, int v) { return std::make_pair(p.second, v); });

    // sort both vectors based on end
    std::sort(
        intervals.begin(), intervals.end(),
        [](const auto& p1, const auto& p2) { return p1.second < p2.second; });
    std::sort(
        end_volumes.begin(), end_volumes.end(),
        [](const auto& p1, const auto& p2) { return p1.first < p2.first; });

    // Bottom up DP: end_volumes[][1] doubles up as the max accumulated volume
    auto prev_it{end_volumes.begin()};  // one past last event before start
    auto curr_it{end_volumes.begin()};  // tracks the index in intervals
    for (const auto& [start, _] : intervals) {
        for (; prev_it->first <= start; ++prev_it) {
        }
        if (prev_it != end_volumes.begin()) {
            curr_it->second += std::prev(prev_it)->second;
        }
        curr_it->second = std::max(curr_it->second, std::prev(curr_it)->second);
        ++curr_it;
    }
    return end_volumes.back().second;
}

int main() {
    vector<int> start{1, 5, 12, 16, 1, 2};
    vector<int> duration{9, 7, 6, 2, 1, 15};
    vector<int> volume{10, 20, 40, 20, 3, 48};
    int res = phoneCalls(start, duration, volume);
    int res2 = phoneCalls2(start, duration, volume);
    cout << "Expected: 63 Actual1: " << res << " Actual2: " << res2 << endl;
    
    duration[1] = 9;
    res = phoneCalls(start, duration, volume);
    res2 = phoneCalls2(start, duration, volume);
    cout << "Expected: 51 Actual1: " << res << " Actual2: " << res2 << endl;
    return 0;
}