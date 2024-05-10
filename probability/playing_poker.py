"""
A few fun results about poker probabilities
"""


import matplotlib.pyplot as plt
from utils.binom import *


"""
Say you are playing a game like BS Poker and you need 2 clubs from the remaining players to 
make a flush. Let's assume you have 4 cards in your hand, so 3 of them are clubs. There are
N other cards you can't see out of 48, and out of them, 10 clubs. In real poker, we can 
imagine that the flop contained a card that matched the suit of your opening hand.

By complementation, P(At least 2 clubs) = 1 - P(No clubs) - P(exactly one club)
"""


def prob_flush(N):
    return 1 - (mCn(38, N) / mCn(48, N)) - (10 * mCn(38, N - 1)) / mCn(48, N)


"""
In (real) poker it is also well-known that straights are about twice as common as flushes. 
However, when you have a 3-card straight draw, the probabiliy of getting the other two numbers 
is significantly lower than getting two of the desired suit, unless you have 3 connecting 
cards in the middle such that 3 straights are possible. By conditional probability, it must be 
easier to get 3 consecutive cards in the first place than 3 of the same suit.

We illustrate the probability of getting 2 of the required cards from the other N hidden cards,
i.e. for A , B, <C, D, E>, F, G, the probability of getting AB, BF, OR FG. This can be done
with inclusion and exclusion: P(AB OR BF OR FG) = P(AB) + P(BF) + P(FG) - P(ABF) - P(BFG), where

P(BF) = P(BG) = P(AB) = 1 - P(no A) - P(no B) + P(no A and no B)
P(BFG) = P(ABF) = -2 + P(no A) + P(no B) + P(no F) + P(AB) + P(BF) + P(AF) - P(no A and no B and no F)

General case:
https://math.stackexchange.com/questions/1708271/how-to-calculate-the-probability-of-getting-at-least-one-of-each-card-in-a-given
"""


def prob_straight1(N):
    return 1 - 2 * (mCn(44, N) / mCn(48, N)) + (mCn(40, N) / mCn(48, N))


def prob_straight2(N):
    AB = prob_straight1(N)
    ABF = -2 + 3 * (mCn(44, N) / mCn(48, N)) + 3 * AB - (mCn(36, N) / mCn(48, N))
    return 2 * AB - ABF


def prob_straight3(N):
    AB = prob_straight1(N)
    ABF = -2 + 3 * (mCn(44, N) / mCn(48, N)) + 3 * AB - (mCn(36, N) / mCn(48, N))
    return 3 * AB - 2 * ABF
    # return 3 * (4 * 4 * mCn(46, N - 2) / mCn(48, N)) - 2 * (4 * 4 * 4 * mCn(45, N - 3) / mCn(48, N))


# PIE can handle P(at least 1 A and at least 1B). Label the A's A1 - A4 and the B's B1 - B4. Then
# our atoms are combinations containing 1 A and 1 B, say {A1, B2}. Each valid combination (e.g.
# {A1, A2, B1, B2}) is formed by the intersection of a unique set of atoms (of size 4 in our example).
# Moreover we don't have to distinguish between {A1, A2, B1, B2} and {A3, A4, B3, B4} so we apply
# mCn(4, i) and mCn(4, j) within the for loop.
def prob_straight1_slow(N):
    denominator = mCn(48, N)
    numerator = 0
    for i in range(1, 5):
        for j in range(1, 5):
            numerator += (
                (-1) ** (i + j) * mCn(4, i) * mCn(4, j) * mCn(48 - i - j, N - i - j)
            )

    return numerator / denominator


# PIE can handle P(at least 1A and 1B OR at least 1B and 1C) but we have to choose atoms carefully.
# If we choose {A1, B1}, {B1, C1} etc. as our atoms, then with a set like {A1, B1, B2, C1}, it could
# be formed by intersecting {{A1, B1}, {A1, B2}, {B2, C1}} or {{A1, B1}, {B2, C1}}, so we can't loop
# through all the pieces cleanly. In other words, we need our atoms to be disjoint in their identifying
# elements. One idea is to choose {A1, B1, no C}, {A1, B1, C1}, and {no A, B1, C1} etc. as our atoms.
# Then pieces with no C, no A and both A and C are formed from the three types of atoms respectively.
def prob_straight2_slow(N):
    denominator = mCn(48, N)
    numerator = 0
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, 5):
                if i > 0 and j > 0 and k == 0:
                    numerator += (
                        (-1) ** (i + j)
                        * mCn(4, i)
                        * mCn(4, j)
                        * mCn(48 - 4 - i - j, N - i - j)
                    )
                if i == 0 and j > 0 and k > 0:
                    numerator += (
                        (-1) ** (j + k)
                        * mCn(4, j)
                        * mCn(4, k)
                        * mCn(48 - 4 - j - k, N - j - k)
                    )
                if i > 0 and j > 0 and k > 0:
                    numerator += (
                        (-1) ** (i + j + k + 1)
                        * mCn(4, i)
                        * mCn(4, j)
                        * mCn(4, k)
                        * mCn(48 - i - j - k, N - i - j - k)
                    )
                # if j ==0 or (i == 0 and k == 0) continue
    return numerator / denominator


# To handle (A and B) OR (B and C) OR (C and D) with PIE, we need eight types of atoms. Using x to
# denote that a letter is absent, we have the following:
# ABxx, ABxD, xxCD, AxCD, xBCx, ABCx, xBCD, ABCD. Instead of implementing the function, we can
# check the output using the sim.r file.
def prob_straight3_slow(N):
    denominator = mCn(48, N)
    numerator = 0
    if N > 0:
        raise NotImplementedError
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, 5):
                for l in range(0, 5):
                    continue  # use the same idea
    return numerator / denominator


"""
Finally, suppose you have two pairs in your 4-card hand, and you want to make a full house with a
triplet of the larger card.
"""


def prob_fullhouse(N):
    return 1 - (mCn(46, N) / mCn(48, N))


Ns = list(range(49))  # N = 0, 1 should give trivially prob = 0
data = []
data.append(["flush", [prob_flush(N) for N in Ns]])
data.append(["straight1", [prob_straight1(N) for N in Ns]])
data.append(["straight2", [prob_straight2(N) for N in Ns]])
data.append(["straight3", [prob_straight3(N) for N in Ns]])
data.append(["full house", [prob_fullhouse(N) for N in Ns]])

legend = []
for name, probs in data:
    plt.plot(Ns, probs, ":")
    legend.append(name)

data = []
# data.append(["straight1_slow", [prob_straight1_slow(N) for N in Ns]])
# data.append(["straight2_slow", [prob_straight2_slow(N) for N in Ns]])
for name, probs in data:
    plt.plot(Ns, probs, ".")
    legend.append(name)
plt.legend(legend)
plt.show()
