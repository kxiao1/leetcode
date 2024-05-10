# Coin Change
# You are given coins of different denominations and a total amount of money. 
# Write a function to compute the number of combinations that make up that amount. 
# You may assume that you have an infinite number of each kind of coin.
def change(amount, coins):
    """
    :type amount: int
    :type coins: List[int]
    :rtype: int
    """

    memo = [0] * amount
    count = 0
    if amount == 0:
        return 1
    for lastOpt in coins: # use only denominations up to lastOpt
        value = lastOpt
        newMemo = [0] * amount
        while value <= amount: # use lastOpt th coin an increasing number of times 
            if value == amount:
                count += 1
            else: 
                newMemo[value] += 1
                residual = amount - value
                if memo[residual] > 0:
                    count += memo[residual]
                for x in range(1, residual):
                    newMemo[x + value] += memo[x]
            value += lastOpt
        memo = [sum(x) for x in zip(memo, newMemo)]
    return count