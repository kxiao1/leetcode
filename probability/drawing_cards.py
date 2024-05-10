"""
Let's say you have a standard deck of 26 red cards and 26 black cards. You draw cards from the
deck without replacement, and if you draw a red card, you get $1, but on a black card you lose
$1. You can stop when the desk runs out, or any time before. What is your optimal strategy, and
how much would you expect to make if you followed that strategy?

A rigorous answer treats the deck of cards as an American option and prices the game via backward
induction. The answer is definitely correct, but it has two drawbacks:
- The method is relatively slow at O(n^2), and
- The exact strategy requires roughly O(n) space, where n = 26 here.

Is there a less profitable but simpler strategy (that doesn't compute the entire tree)? As a
heuristic, let V(s, n) be the value of the game when the sum of your returns is $s, and you have
n red cards left to draw. Clearly V(0, n) = 0 if n = 0. When s = 0, n > 0, note that V(s, n)
>= 1/2. This comes from the following strategy: if the next card you draw is red, you can stop and 
get $1. Otherwise, finish the deck and get $0. So we should never stop when s = 0, n > 0, and we 
should most certainly not when s < 0.

With a lower bound for V(0, n), we can determine a lower bound for V(1, n) and determine N1 such
that we stop at (1, n) when n < N1. We can iteratively determine lower bounds for V(2, n), V(3, n)
and so on, but we will stop at 3 here for simplicity. V(1, n) and V(2, n) are not hard to bound
with algebra, and we use a linear search for V(3, n). In the following V1(n) computes V(1, n) etc.
Note that N1, N2's here are also underestimates because we are not aggressive enough.

This strategy attains an average of 2.268 with 10^7 trials of play_simply, compared to an expected 
payoff of 2.624 under the optimal strategy, which we derive below and test with play_optimally.
So the simple strategy is around 85% as good as the optimal, meaning that all that extra
optimization brought diminishing marginal returns.
"""
import numpy as np


def V0(n: int):
    return 0.5 if n >= 1 else 0.0


# (n - 1) / (2 * (2n + 1)), continue if n >= 1
def V1(n):
    return n / (2 * n + 1) + (n + 1) / (2 * n + 1) * (-1 + V0(n))


# (n^2 - 7n - 6) / (4(2n + 1)(n + 1)), continue if n >= 8
def V2(n):
    return n / (2 * n + 2) + (n + 2) / (2 * n + 2) * (-1 + V1(n))


# s = 3 threshold determined below
def V3(n):
    return n / (2 * n + 3) + (n + 3) / (2 * n + 3) * (-1 + V2(n))


def calibrateV3():
    n = 1
    while V3(n) < 0:
        n += 1
    return n


t1 = 1
t2 = 8
t3 = calibrateV3()


# We use our crude strategy
def play_simply(deck):
    s = 0  # running score
    n = 26  # number of red cards left
    for i in deck:
        s += i
        n -= max(i, 0)
        if s <= 0:
            continue
        if s == 1 and n < t1:
            break
        if s == 2 and n < t2:
            break
        if s == 3 and n < t3:
            break
        if s >= 4:
            break
    return s


def getOptimalPayoff(n=52):
    intrinsics = []
    grid = []
    for i in range(n + 1):
        amp = n // 2 - abs(n // 2 - i)
        # initializing with return at that node helps to calculate probabilities
        intrinsics.append(list(range(-amp, amp + 1, 2)))
        grid.append([0] * (amp + 1))

    for t in range(n - 1, -1, -1):
        row = grid[t]  # we will overwrite with the "value" of that point (0 if stop)
        if len(row) > len(grid[t + 1]):
            for i, val in enumerate(intrinsics[t]):
                if i == len(grid[t]) - 1:
                    row[i] = max(0, -1 + grid[t + 1][-1])
                elif i == 0:
                    row[i] = max(0, 1 + grid[t + 1][0])
                else:
                    p = (n - t - val) / (2 * (n - t))
                    q = 1 - p
                    row[i] = max(
                        0, p * (1 + grid[t + 1][i]) + q * (-1 + grid[t + 1][i - 1])
                    )
        else:
            for i, val in enumerate(intrinsics[t]):
                p = (n - t - val) / (2 * (n - t))
                q = 1 - p
                row[i] = max(
                    0, p * (1 + grid[t + 1][i + 1]) + q * (-1 + grid[t + 1][i])
                )

    frontier = [-1] * (n + 1)
    for i in range(n, -1, -1):
        thres = -1
        for j, val in enumerate(grid[i]):
            if val == 0:
                num_red_left = (52 - i - intrinsics[i][j]) // 2
                frontier[intrinsics[i][j]] = num_red_left
                break
    # print("Theoretical best N1, N2...'s")
    # for i in range(7):
    #     print("N"+str(i), frontier[i])
    return frontier, grid[0][0]


thresholds, value = getOptimalPayoff(52)
print("Optimal exercise thresholds", thresholds)
print("Optimal strategy payoff (theoretical)", value)


def play_optimally(deck):
    s = 0
    n = 26
    for i in deck:
        s += i
        n -= max(i, 0)
        if s <= 0:
            continue
        if s == 1 and n <= 1:
            break
        if s == 2 and n <= 3:
            break
        if s == 3 and n <= 7:
            break
        if s == 4 and n <= 12:
            break
        if s == 5 and n <= 18:
            break
        if s >= 6:
            break  # break whenever s reaches 6
    return s


rng = np.random.default_rng()
deck = np.array([-1] * 26 + [1] * 26)
print("deck (-1 = black, 1 = red) = \n", deck)

### By Stirling's approx, total combinations ~1/sqrt(pi * 26) * 2 ** 52 ~= 5e15
num_trials = int(1e7)  # with this many iterations, the for loop will be slow
mean = 0.0
mean2 = 0.0
for i in range(num_trials):
    mean = mean * i / (i + 1) + play_simply(rng.permutation(deck)) / (i + 1)
    mean2 = mean2 * i / (i + 1) + play_optimally(rng.permutation(deck)) / (i + 1)
print("Easy strategy payoff", mean)
print("Optimal strategy payoff", mean2)
