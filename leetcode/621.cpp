// https://leetcode.com/problems/task-scheduler/description/?source=submission-ac

#include <vector>
int leastInterval(std::vector<char>& tasks, int n) {
    /*
        We know that tasks that appear most frequently, say k times, are the
       bottleneck so we schedule them first We need to respect the spacing
       requirements (one task every n + 1 units), but if there are N > n + 1
        tasks that appear k times, we can run t1, t2... tN, t1, t2... tN and so
       on to avoid any idle time. This serves as a lower bound on the number of
       steps needed.

        After this process, we will fill in the remaining idle time with other
       tasks. If there are at least as many tasks as holes, then we can use the
       same trick of inserting tasks between each run of t1... tN as needed. So
       now our schedule has no holes at all and the count is the number of
       tasks. Otherwise, there are more holes than tasks, so we will return the
       previous bound.

        Ultimately, we have two cases: no holes, and with holes.

    */
    std::vector<int> counts(256);  // 1 char = 8 bits and assume int big enough
    for (auto c : tasks) {
        ++counts[c];
    }
    int max_cnt{0}, cnt_max_cnt{0};
    for (auto count : counts) {
        if (count == max_cnt) {
            ++cnt_max_cnt;
        }
        if (count > max_cnt) {
            cnt_max_cnt = 1;
            max_cnt = count;
        }
    }
    return std::max((n + 1) * (max_cnt - 1) + cnt_max_cnt, (int)tasks.size());
}

int main(){};