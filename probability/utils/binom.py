"""
Some helper functions for combinatorial analysis
"""


# Calculate n * (n-1) * ... (n-k+1)
def partialFac(n, k):
    res = 1
    while k > 0:
        res *= n - k + 1
        k -= 1
    return res


# requires m > 0
# returns 0 if n < 0 or m < n, else \binom{m}{n}
def mCn(m, n):
    n = min(n, m - n) % (max(n, m - n) + 1)
    return partialFac(m, n) / partialFac(n, n)
