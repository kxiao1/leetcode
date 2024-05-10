"""
Two players A and B each choose a number between 1 and 100.
An umpire then chooses randomly a base b between 1 and 100.
Player A wins if A mod b > B mod b, and vice versa.
1) What is the expected value for A and B?
- 0 for both (it is a fair game)
2) Is there an optimal number that A and B should both choose (i.e. pure strategy)?
- No: For every number A choose, B can make it suffer (e.g. B = A + 1, except when A = 100)
- Minimax is 100 (worst case -52 if B chooses 47 or 53 - primes do well against random strategies)
- Expectimax is 47(!) - expected return = 24.57 if B chooses randomly
3) Is there a mixed strategy?
- There are many optimal mixed strategies because we do not have enough binding constraints
- Important numbers include 47, 59, 71, 77, 83, 89, 95: these add up to >75% total weight
"""

import math
from scipy import optimize


# for every b, add 1 to A's score if A wins, 0 if draw, -1 if B wins
def compare(AA, BB):
    score = 0
    for b in range(1, 101):
        A = AA % b
        B = BB % b
        if A > B:
            score += 1
        if A < B:
            score -= 1
    return score


# min_and_opp[i - 1] = [a, b, j] means that if A plays a, his worst score is j if B plays b
min_and_opp = []
max_and_opp = []
avg = []


def compute_pure_strategies():
    for A in range(1, 101):
        min_score = 100
        min_idx = -1
        max_score = -100
        max_idx = -1
        total_score = 0
        for B in range(1, 101):
            score = compare(A, B)
            total_score += score
            if score < min_score:
                min_score = score
                min_idx = B
            if score > max_score:
                max_score = score
                max_idx = B
        min_and_opp.append([A, min_idx, min_score])
        max_and_opp.append([A, max_idx, max_score])
        avg.append([A, total_score / 100])

    k = lambda x: x[-1]
    print("Minimax", max(min_and_opp, key=k))
    print("Minimin", min(min_and_opp, key=k))
    print("Maximax", max(max_and_opp, key=k))
    print("Maximin", min(max_and_opp, key=k))
    print("Expectimax", max(avg, key=k))
    print("Full mins", min_and_opp)
    print("Full maxes", max_and_opp)
    print("Avgs", avg)


def get_non_zeros(arr):
    return [(i, math.floor(x * 1e5) / 1e5) for i, x in enumerate(arr) if i > 0 and abs(x) > 1e-5]

# see ibet.cpp for transforming zero-sum games into LPs
def compute_mixed_strategies():
    A = [[0] * 101 for _ in range(101)]
    offset = 100
    for a in range(1, 101):
        for b in range(1, 101):
            A[a - 1][b] = -compare(b, a) - offset  # ensure all entries are negative
    for i in range(100):
        A[i][0] = 1
        A[-1][i + 1] = 1

    B = [0] * 101
    B[-1] = 1

    # https://stackoverflow.com/questions/30849883/linear-programming-with-scipy-optimize-linprog
    C = [0] * 101
    C[0] = -1  # flipped

    # print(A, B, C)

    out = optimize.linprog(c=C, A_ub=A, b_ub=B, method="highs")
    non_zeros = get_non_zeros(out.x)
    print("value:", out.fun + offset)
    print("unperturbed strat:", non_zeros)

    # https://andrewpwheeler.com/2021/10/24/generating-multiple-solutions-for-linear-programs/
    for i, x in non_zeros:
        bounds = [(0, None)] * 101
        bounds[i] = (0, math.floor(x * 1e3) / 1e3)
        out_perturbed = optimize.linprog(c=C, A_ub=A, b_ub=B, bounds=bounds, method="highs")
        # print(bounds)
        print("perturbed", i, "strat:", get_non_zeros(out_perturbed.x))


compute_pure_strategies()
compute_mixed_strategies()

score47 = [0] * 101
for B in range(1, 101):
    score47[B] = (B, compare(47, B))
print("47 Profile", score47)

score100 = [0] * 101
for B in range(1, 101):
    score100[B] = (B, compare(100, B))
print("100 Profile", score100)
