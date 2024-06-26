// #pragma once  // not used if compiles as a cpp file with C++20 modules

export module linked_list;
/* Linked list interface. */
export class LinkedList {
   public:
    // virtual destructor
    virtual ~LinkedList() = default;

    // Returns start of the list; returns nullptr iff total_size = 0.
    virtual void *head() const = 0;
    // Returns ptr->next. It is up to the caller to ensure that ptr is not null.
    virtual void *move(void *ptr) const = 0;

    // Conceptually equivalent to setting curr->next to next. This method allows
    // arbitrary modification of the list and underlies one possible solution.
    virtual void make_next(void *curr, void *next) = 0;
};