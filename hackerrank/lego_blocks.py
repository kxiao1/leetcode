# https://www.hackerrank.com/challenges/lego-blocks/problem


def legoBlocks(n, m):
    b = 10**9 + 7

    # number of combinations per row, top down DP
    combis = [0] * (m + 1)  # width = m
    combis[0] = 1
    for i in range(1, m + 1):
        for j in range(1, min(i, 4) + 1):
            combis[i] = (combis[i] + combis[i - j]) % b
    # scale by number of rows (n)
    totals = [pow(v, n, b) for v in combis]

    # now subtract the number of bad combinations
    # case on where the first 'crack' occurs, so before the crack all's good
    goods = totals[:]

    for i in range(1, m + 1):
        for j in range(1, i):
            goods[i] = (goods[i] - goods[j] * totals[i - j] + b) % b

    return goods[m]
