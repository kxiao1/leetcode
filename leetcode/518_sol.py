# same idea of bottom-up DP, but much cleaner
# don't bother with intermediate counts
# when x is some multiple k of coin, it automatically
# adds to the combinations of using (k-1) of coin
from typing import List
def change(amount: int, coins: List[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1
        
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]
    return dp[amount]