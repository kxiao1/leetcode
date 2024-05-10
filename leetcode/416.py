# Given a non-empty array nums containing only positive integers,
# find if the array can be partitioned into two subsets such that
# the sum of elements in both subsets is equal.
def canPartition(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    nums.reverse()
    s = sum(nums)
    l = len(nums)
    if s % 2 == 1:
        return False
    half = s / 2
    memo = dict()
    numCalls = [0]

    def help(idx, s):
        if s in memo.keys():
            return memo[s] # only need to store remaining sum
        if s == 0:
            return True
        if  idx == 0:
            return False
        numCalls[0] += 1
        print(idx, s)
        curr = nums[idx - 1]
        if curr > s:
            res = help(idx - 1, s)
        else:
            res = help(idx - 1, s - curr) or help(idx - 1, s)
        memo[s] = res
        return res

    ans = help(l, half)
    print(len(nums), len(memo.keys()), numCalls)
    return ans

print(canPartition([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 
                    # 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 
                    100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 97, 99]))
