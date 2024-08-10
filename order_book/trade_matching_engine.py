"""
In my solution, I store resting bids and offers in separate flat lists. Both lists are ordered
from best to worse, so offers are sorted in ascending price level while bids are sorted in
descending price level. Each level object (Level) consists of a price and the list of orders at
that level. I use a deque to store and access the orders according to FIFO logic.

According to the specs, incoming orders are matched against the opposing book first. By storing
bids and offers each in a particular order, I am able to traverse both of them from front to back.
Any remaining limit order is then stored in "my_book". Here, I ensure that the list is sorted by
always inserting a new order level at its index in the sorted list. I find the index using a linear
search, following the assumption that real-world bids and offers are usually placed near the best
price. An alternative is to run a binary search; it is faster in theory but likely to be slower
in practice.

Lastly, I really wanted to solve this problem in C++ using (ordered) maps for bids and offers
instead of flat lists. Unfortunately, that was not an option.
"""

from collections import deque  # to store FIFO orders
from sys import stdin, stdout  # I/O
from operator import lt, gt  # to implement comparisons between bids and offers


def solve():

    # Represents an unfulfilled ("resting") limit order. Since we always print the timestamp of the
    # matching order, we don't need to store the timestamp of a resting order.
    class Order:
        def __init__(self, client_id, size):
            self.client_id = client_id
            self.size = size

    # Represents a price level together with its Order's (bids or offers).
    class Level:
        def __init__(self, px, od):
            self.price = px
            self.orders = deque([od])

    # Helper method to print completed trades.
    def print_trade(time, new_id, resting_id, bs, price_raw, size_raw):
        price = f"{price_raw:.2f}"  # force price to be printed with 2 decimals
        size = str(size_raw)
        if bs == "b":  # new_id is buyer, so it is listed first
            line = " ".join([time, new_id, resting_id, price, size, "\n"])
        else:  # new_id is seller, so it is listed later
            line = " ".join([time, resting_id, new_id, price, size, "\n"])
        stdout.write(line)  # alternatively we can just use print?

    bids = []  # to be filled with Level's
    offers = []

    stdin.readline()  # discard the first number
    for line in stdin:
        time, client_id, bs, tot_size_raw, order_type, px_raw = line.split(" ")
        tot_size = int(tot_size_raw)
        px = float(px_raw)

        # leverage the symmetry between a bid filling offers and vice versa
        if bs == "b":
            my_book, other_book = bids, offers
            worse_cmp = lt  # a bid is worse if it's lower than the other price
        else:
            my_book, other_book = offers, bids
            worse_cmp = gt  # an offer is worse if it's higher than the other price

        # for a market order, assume price equals max price (i.e. highest bid or lowest offer)
        if px < 0 and len(other_book) > 0:
            px = other_book[-1].price

        # try to match against the other book first
        for level in other_book:
            if tot_size <= 0 or worse_cmp(px, level.price):
                break
            while tot_size > 0 and len(level.orders) > 0:
                od = level.orders.popleft()
                size_filled = min(tot_size, od.size)
                print_trade(time, client_id, od.client_id, bs, level.price, size_filled)
                tot_size -= size_filled
                od.size -= size_filled
                if od.size > 0:
                    level.orders.appendleft(od)  # add the remaining resting order back

        # ignore a partially filled market order or fully filled limit order
        if order_type == "m" or tot_size == 0:
            continue

        # Update my_book with "insertion sort"
        # "while ()" is slightly shorter than "for level in my_book:"
        insertion_idx = 0
        my_od = Order(client_id, tot_size)
        while insertion_idx < len(my_book) and worse_cmp(px, my_book[insertion_idx].price):
            insertion_idx += 1
        if insertion_idx < len(my_book) and px == my_book[insertion_idx].price:
            my_book[insertion_idx].orders.append(my_od)
        else:
            my_book.insert(insertion_idx, Level(px, my_od))

    return


if __name__ == "__main__":
    solve()
