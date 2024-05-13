// #include "linked_list.h"
import linked_list;

/* Task: Find the length of a singly linked list ll.*/
class Solution {
   public:
    Solution(LinkedList &ll);
    int solve();

   private:
    // We could also move and store ll as a value if LinkedList weren't virtual
    LinkedList &l;  // borrow the same list

    struct c_ptr;
    bool move_fast(c_ptr &f);
    bool move_slow(c_ptr &s);
};