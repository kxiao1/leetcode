#include <concepts>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <tuple>
#include <variant>

/* Proof of concept solution with trees, otherwise imitating the python code */
struct Order {
    std::string client_id;
    int size;
};

// Experimental!! https://en.cppreference.com/w/cpp/iterator/iterator_tags
// I guess the more the better...
// Also, "The definition of a concept must appear at namespace scope."
template <typename T>
concept OrderBook = std::bidirectional_iterator<typename T::iterator> &&
                    std::same_as<typename T::key_type, double> &&
                    std::predicate<typename T::key_compare, double, double> &&
                    // or std::same_as<typename T::mapped_type, queue<Order>
                    std::same_as<typename T::mapped_type::value_type, Order> &&
                    requires(T::mapped_type t) {
                        { t.front() } -> std::same_as<Order&>;
                    };
class Engine {
   public:
    void match() {
        std::string line;
        std::getline(std::cin, line);  // discard the first line

        while (std::getline(std::cin, line)) {
            // either auto or const auto& or auto&&, cannot normal ref a rvalue!
            // order_type can be deduced from the px (<0 = market)
            auto [time, client_id, bs, tot_size, _, px] = parse_order(line);

            // Sadly, C++'s type system (iterator != reverse_iterator !=
            // const_reverse_iterator, map<_, _, greater> != map<_, _, less>)
            // makes it hard to implement the Python my_book, other_book hack
            // std::variants don't work: must call std::get<typename> before use
            // So either abstract out the template args of 'bids' and 'offers',
            // or define a "OrderBook" concept and auto the rest out!
            if (bs == 'b') {
                fill_order(px, tot_size, time, client_id, bs, offers, bids);
            } else {
                fill_order(px, tot_size, time, client_id, bs, bids, offers);
            }

            // Experimental! We can do the same 'if' but now without templates.
            fill_order_test(px, tot_size, time, client_id, bs, bids, offers);
        }
    }

   private:
    std::map<double, std::queue<Order>, std::greater<double>> bids;  // decr
    std::map<double, std::queue<Order>, std::less<double>> offers;   // incr

    template <typename OtherCmp, typename MyCmp>
    // requires std::predicate<OtherCmp, double, double> &&
    // std::predicate<MyCmp, double, double> // implied by std::map<double...>
    void fill_order(double my_price, int my_size, std::string time,
                    std::string client_id, char bs,
                    std::map<double, std::queue<Order>, OtherCmp>& other_book,
                    std::map<double, std::queue<Order>, MyCmp>& my_book) {
        OtherCmp worse_cmp;  // don't write worse_cmp() --> most vexing parse

        bool is_limit_order{my_price > 0};
        if (my_price < 0 && other_book.size() > 0) {
            my_price = other_book.rbegin()->first;
        }

        // alternatively, put breaking condition in for loop guard
        for (auto& level : other_book) {
            auto& [level_price, orders] = level;
            if (my_size <= 0 || worse_cmp(my_price, level_price)) {
                break;
            }
            while (my_size > 0 && orders.size() > 0) {
                Order& od{orders.front()};
                int size_filled{std::min(my_size, od.size)};
                print_trade(time, client_id, od.client_id, bs, level_price,
                            size_filled);
                my_size -= size_filled;
                od.size -= size_filled;
                if (od.size == 0) {
                    orders.pop();  // we remove a filled order
                }
            }
        }

        if (is_limit_order && my_size > 0) {
            // less code than auto [it, _] = my_book.insert_or_assign(...)
            my_book[my_price].emplace(client_id, my_size);
        }
    }

    // Again, Experimental
    bool fill_order_test(double my_price, int my_size, std::string time,
                         std::string client_id, char bs,
                         OrderBook auto other_book, OrderBook auto my_book) {
        typename decltype(other_book)::key_compare worse_cmp;
        // This shows that everything else in fill_order should work
        return worse_cmp(other_book.begin()->first, 0);
    }

    std::tuple<std::string, std::string, char, int, char, double> parse_order(
        std::string line) {
        return {"", "", 0, 0, 0, 0.0};  // TODO: same logic as Python
    }
    void print_trade(std::string time, std::string new_id,
                     std::string resting_id, char bs, double price, int size) {
        std::cout << "To be implemented";  // TODO: same logic as Python
    }
};

int main() {
    Engine E;
    E.match();
}