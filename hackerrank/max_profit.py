def dp(saving, currentValue, profit, memo, idx):
    prev = 0
    if idx == 0:
        return 0
    if memo[idx][saving] != -1:
        return memo[idx][saving]
    result = 0
    if currentValue[idx-1] > saving:
        result = dp(saving, currentValue, profit, memo, idx-1)
    else:
        result = max(profit[idx-1] + dp(saving - currentValue[idx-1], currentValue, profit, memo, idx - 1),
                     dp(saving, currentValue, profit, memo, idx - 1))
    memo[idx][saving] = result
    return result


def selectStock(saving, currentValue, futureValue):
    # Write your code here

    # dynamic programming
    profit = [0] * len(currentValue)
    for i in range(len(currentValue)):
        profit[i] = futureValue[i] - currentValue[i]
    memo = [[-1 for x in range(saving + 1)]]*(len(currentValue) + 1)
    res = dp(saving, currentValue, profit, memo, len(currentValue))
    return res

def main():
    saving = 10
    currentValue = [2,3,4,5,6]
    futureValue = [10,8,12,4,3]
    res = selectStock(saving, currentValue, futureValue)
    ans = 10
    if res != ans:
        print("Wrong answer, Expected:", ans, "Actual:", res)
    else:
        print("PASS")

if __name__ == "__main__":
    main()