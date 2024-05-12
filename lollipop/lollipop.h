#include "linked_list.h"

/* A minimal singly linked list. It is called a lollipop because the list can
 * have at most one loop that does not extend beyond the intersection.*/
class Lollipop : public LinkedList {
   public:
    // total_size >= loop_size >= 0
    Lollipop(int total_size, int loop_size);

    // move constructor and assignment
    Lollipop(Lollipop &&other);
    Lollipop &operator=(Lollipop &&other);

    // delete copy constructor and assignment
    Lollipop(const Lollipop &other) = delete;
    Lollipop &operator=(const Lollipop &other) = delete;

    virtual ~Lollipop();

    virtual void *head() const override;
    virtual void *move(void *ptr) const override;
    virtual void make_next(void *curr, void *next) override;

   private:
    void **list;
};
