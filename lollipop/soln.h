#include "lollipop.h"
class Solution {
   public:
    Solution(Lollipop &ll);
    int solve();

   private:
    // alternatively store value and call move constructor
    Lollipop &l;  // borrow the same lollipop

    struct c_ptr;
    bool move_fast(c_ptr &f);
    bool move_slow(c_ptr &s);
};