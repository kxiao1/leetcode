"""
Given n, generate the first n Hamming numbers (5-smooth numbers) in ascending order.

Code inspiration:
http://svn.python.org/projects/python/trunk/Lib/test/test_generators.py

The code has been updated to Python 3 and all comments/ printds are mine.

IDEA
- H = {1} at the beginning
- Each of me_times2, me_times3, and me_times5 keeps an index into H, intially all index 0
- Each N (2, 3 or 5) will propose a candidate, and when N's candidate is chosen, increment N's index

The classic solution by Dijkstra creates the size O(3^n) non-combining tree e.g. in Haskell
merge :: [Int] -> [Int] -> [Int]
merge xs [] = xs
merge [] xs = xs
merge (x:xs) (y:ys)
 | x < y = x : merge xs (y:ys)
 | x > y = y : merge (x:xs) ys
 | otherwise = x : merge xs ys

ham = 1 : merge (map (*2) ham)
                (merge (map (*3) ham)
                       (map (*5) ham))

(https://medium.com/@romandobrovenskii/hamming-numbers-and-haskell-b0b6b6701222)

However, it is claimed ([1]) that Haskell could do the same 'pointers' approach.

A similar solution that uses 3 caches instead of 1 is described at
https://11011110.github.io/blog/2007/03/12/hammings-problem.html. One advantage is that 6, for
instance, will only be generated as 2 x 3 and not 3 x 2. I don't really understand the claimed
time and space complexities. The 'ETA2' solution is essentially the imperative version of what 
I have here.

Naive method: Take n and test each number.

MATH QUESTION
Show that the gap between consecutive Hamming numbers can be arbitrarily large.

PROOF (non-constructive)
- Consider the range [1, 2^n].
- The set of Hamming numbers in this range is a subset of {2^i * 3^j * 5^k, i + j + k <= n}
- The number of ways to choose 3 numbers that sum to at most n is given by the "stars and bars"
formula (Theorem 2 of https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)) as (n+3) C 3
- Alternatively, by conditioning and induction, we obtain explicitly (n+1)(n+2)(n+3) / 6.
- Thus, there are at most (n+1)(n+2)(n+3) / 6 (=: D) Hamming numbers up to 2^n (=: N).
- Now by the Pigeonhole principle, if I divide [1, 2^N] into D + 1 boxes, each of size at least 
floor(N / (D+1)), at least one box will be empty.
- It is clear that 2^n/n^3 --> 0 as n --> infty, so we can find arbitrarily large empty boxes.
- Lastly, an empty box of size k means that k consecutive numbers are not Hamming numbers,
concluding the proof. 

Other references: 
[1] http://lambda-the-ultimate.org/node/608, 
[2] https://blog.ganssle.io/articles/2021/10/regular-numbers-in-python.html

"""

DDEBUG = True

def printd(s):
    if DDEBUG:
        print(s)

def times(n, g):
    printd("Entered times {0}".format(n))
    for i in g:
        printd("got {0} from g and multiplying by {1}".format(i, n))
        yield n * i


# yields an ordered list of results from generators g and h
def merge(g, h):
    printd("entering merge function")
    ng = next(g)
    nh = next(h)
    while 1:
        printd("merging {0} and {1}".format(ng, nh))
        if ng < nh:
            yield ng
            ng = next(g)
        elif ng > nh:
            yield nh
            nh = next(h)
        else:
            yield ng
            ng = next(g)
            nh = next(h)


class LazyListHamming:
    def __init__(self):
        self.sofar = []
        self.g = self.m235() # nothing in m235 gets run, not even the print statement
        print("Initialized the lazy list")
    def m235(self):
        printd("yielding the first number")
        yield 1
        printd("creating 3 implementors")  # this line is only printded once
        me_times2 = times(2, self)  # recurse on the class itself ('closure')
        me_times3 = times(3, self)  # times(...) will call __getitem__ but not m235 again
        me_times5 = times(5, self)
        for i in merge(merge(me_times2, me_times3), me_times5):
            printd("yielding subsequent numbers")
            yield i

    # https://stackoverflow.com/questions/926574/why-does-defining-getitem-on-a-class-make-it-iterable-in-python
    def __getitem__(self, i):
        printd("got request for {0}th number".format(i))
        while i >= len(self.sofar):
            self.sofar.append(next(self.g))
        printd(self.sofar)
        return self.sofar[i]


hamming_numbers = LazyListHamming()
# print(hamming_numbers[5000])
print([hamming_numbers[i] for i in range(10)])
