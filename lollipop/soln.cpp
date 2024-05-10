#include "soln.h"

#include <cassert>
#include <iostream>

struct Solution::c_ptr {
    void *ptr{nullptr};  // node
    int cnt{0};          // number of steps taken
    bool operator==(const c_ptr &other) const { return ptr == other.ptr; }
    operator bool() const { return ptr != nullptr; }
};

Solution::Solution(Lollipop &ll) : l(ll) {}

int Solution::solve() {
    c_ptr slow_ptr{l.head()}, fast_ptr{l.head()};

    // step 1) determine if there is a loop, if not return the chain's size
    while (move_fast(fast_ptr) && move_slow(slow_ptr) && fast_ptr != slow_ptr) {
    }
    if (!fast_ptr) {
        // we have reached the end of the chain (no loop to traverse)
        std::cout << std::dec << "chain size: " << fast_ptr.cnt << "\n";
        return fast_ptr.cnt;
    }

    // step 2) determine the size of the loop (including the intersection)
    c_ptr slow_ptr_start = slow_ptr;
    while (move_slow(slow_ptr) && slow_ptr != slow_ptr_start) {
    }
    int loop_size{slow_ptr.cnt - slow_ptr_start.cnt};
    std::cout << std::dec << "loop size: " << loop_size << "\n";

    // step 3a) start another slow_ptr and move the two of them together.
    // They will meet where the stem joins the loop. The distance travelled
    // by slow_2 before they meet is the stem size. In particular, if the
    // list just a loop, slow_ptr will not be moved so stem_size = 0.
    c_ptr slow_2{l.head()};
    while (slow_2 != slow_ptr && move_slow(slow_ptr) && move_slow(slow_2)) {
    }
    int stem_size{slow_2.cnt};
    std::cout << std::dec << "stem size: " << stem_size << "\n";

    // step 3b) alternatively, start a slow_ptr that traverses and reverses
    // the list by itself. Eventually, it will come back to head() having
    // travelled 2 * stem_size + loop_size. The direction of the loop is
    // reversed but this can be undone by another traversal.
    void *slow_curr{l.head()};
    void *slow_prev{nullptr};
    c_ptr slow_next{l.head()};
    while (slow_next) {
        move_slow(slow_next);               // next = curr->next;
        l.make_next(slow_curr, slow_prev);  // curr->next = prev;
        slow_prev = slow_curr;              // prev = curr;
        slow_curr = slow_next.ptr;          // curr = next;
    }
    int new_stem_size = (slow_next.cnt - loop_size) / 2;

    assert(stem_size == new_stem_size);  // the two approaches should agree

    // step 4) size of lollipop = loop size + stem size
    return loop_size + stem_size;
}

bool Solution::move_fast(c_ptr &f) {
    // take up to two steps
    for (int i = 0; i < 2 && f.ptr; ++i) {
        f.ptr = l.move(f.ptr);
        ++f.cnt;
    }
    return f.ptr != nullptr;
}

bool Solution::move_slow(c_ptr &s) {
    if (s.ptr) {
        s.ptr = l.move(s.ptr);
        ++s.cnt;
    }
    return s.ptr != nullptr;
}
