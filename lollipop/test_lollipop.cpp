#include <cassert>
#include <iostream>

#include "soln.h"

void test_lollipop_impl(int tot_size, int loop_size) {
    Lollipop l(tot_size, loop_size);
    void *p = l.head();

    // Move (tot - loop) steps to the start of the loop
    for (int i = 0; i < tot_size - loop_size; ++i, p = l.move(p)) {
    };

    // Move loop_size steps more, should complete a loop
    void *p2 = p;
    for (int i = 0; i < loop_size; ++i, p = l.move(p)) {
    };
    assert(p == p2);

    // Move loop_size steps more, should be back at the same place again
    void *p3 = p;
    for (int i = 0; i < loop_size; ++i, p = l.move(p)) {
    };
    assert(p == p3);

    // Move another pointer (tot - loop) steps from the head, should end at p
    void *p4 = l.head();
    for (int i = 0; i < tot_size - loop_size; ++i, p4 = l.move(p4)) {
    };
    assert(p4 == p);
}

void test_lollipop_soln(int tot_size, int loop_size) {
    std::cout << std::dec << "[TEST] tot_size = " << tot_size
              << ", loop_size = " << loop_size << "\n";
    Lollipop l(tot_size, loop_size);
    Solution s(l);

    assert(tot_size == s.solve());
}

int main() {
    test_lollipop_impl(8, 4);
    test_lollipop_impl(100, 9);
    test_lollipop_impl(77, 1);  // self-loop
    test_lollipop_impl(1, 1);
    test_lollipop_impl(1, 0);
    test_lollipop_impl(0, 0);

    test_lollipop_soln(8, 4);    // even loop
    test_lollipop_soln(12, 7);   // odd loop
    test_lollipop_soln(77, 2);   // small loop
    test_lollipop_soln(79, 25);  // big loop
    test_lollipop_soln(79, 34);  // big loop

    test_lollipop_soln(3, 0);    // no loop
    test_lollipop_soln(100, 0);  // no loop
    test_lollipop_soln(77, 1);   // self-loop
    test_lollipop_soln(78, 78);  // only a loop

    // edge cases
    test_lollipop_soln(2, 2);
    test_lollipop_soln(2, 1);
    test_lollipop_soln(1, 1);
    test_lollipop_soln(1, 0);
    test_lollipop_soln(0, 0);
}