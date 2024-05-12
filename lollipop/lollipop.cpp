#include "lollipop.h"

// import <iostream>; has to work before we can export this as a module
#include <iostream>  // otherwise size_t and std::move are not defined

Lollipop::Lollipop(int total_size, int loop_size) {
    if (total_size < loop_size || loop_size < 0) {
        throw "Invalid lollipop";
    }

    // Need to short circuit here, because dynamically allocating an empty array
    // produces a pointer that cannot be dereferenced yet is not nullptr
    // Using a container, we could return list.begin() even if it were empty
    if (total_size == 0) {
        list = nullptr;
        return;
    }

    // Here we know total_size > 0
    list = new void *[total_size];
    for (int i = 0; i < total_size - 1; ++i) {
        list[i] = static_cast<void *>(list + i + 1);
    }
    if (loop_size > 0) {
        // point the last node to where it intersects the steam, and in a
        // self-loop, (i.e. loop_size = 1), point it back to itself.
        list[total_size - 1] =
            static_cast<void *>(list + total_size - loop_size);
        return;
    } else {
        list[total_size - 1] = nullptr;  // no loop
    }
}

Lollipop::Lollipop(Lollipop &&other) : list(other.list) {
    other.list = nullptr;
};

Lollipop &Lollipop::operator=(Lollipop &&other) {
    return *this = Lollipop(std::move(other));
};

Lollipop::~Lollipop() { delete[] list; }

void *Lollipop::head() const { return static_cast<void *>(list); }
void *Lollipop::move(void *ptr) const { return *static_cast<void **>(ptr); }

void Lollipop::make_next(void *curr, void *next) {
    *static_cast<void **>(curr) = next;
}