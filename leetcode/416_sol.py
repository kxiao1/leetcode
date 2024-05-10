def canPartition(nums):
    if sum(nums) % 2 == 1: return False
    goal = sum(nums) // 2
    memo = set()
    # nums.sort(reverse=True)
    l = len(nums)
    numCalls = [0]
    
    # DFS works because all integers are possible
    # At first the sum decreases as fast as possible
    # If later you come across the same sum, 
    # there will be fewer numbers to work with
    # so if previously it was not possible it still won't be
    def dfs(i, remain):
        print(i, remain, "start")
        if remain == 0: return True
        if remain < 0 or remain in memo: return False            
        numCalls[0]+=1
        print(i, remain)
        for next in range(i+1, l):                
            if dfs(next, remain-nums[next]): return True                 
        memo.add(remain)
        return False
        
    res = dfs(0, goal)
    print(len(nums), len(memo), numCalls)
    return res