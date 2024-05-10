#include <set>
#include <unordered_map>
// https://leetcode.com/problems/stock-price-fluctuation/description/

/* Instead of storing a map of key -> counts, this solution just uses a multiset
 * to get the counts "for free". Using a min priority queue and max priority
 * queue might make the code even faster.*/
class StockPrice {
   public:
    StockPrice() {}

    void update(int timestamp, int price) {
        if (auto it = price_path.find(timestamp); it != price_path.end()) {
            price_counts.erase(price_counts.find(it->second));
        }
        price_counts.insert(price);

        price_path[timestamp] = price;
        curr_time = std::max(curr_time, timestamp);
    }

    int current() { return price_path[curr_time]; }

    int maximum() { return *price_counts.rbegin(); }

    int minimum() { return *price_counts.begin(); }

   private:
    int curr_time{0};
    std::multiset<int> price_counts;  // the count is "automatically" stored
    std::unordered_map<int, int> price_path;  // time -> price
};
