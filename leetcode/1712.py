class Solution(object):
    def binSearch(self, arr, target):
        idx = len(arr) // 2
        start  = 0
        end = len(arr) - 1 
        while (start < end):
            if (arr[idx] == target):
                return idx
            if (arr[idx] < target):
                start = idx + 1
            else:
                end = idx
            idx = (start + end) // 2
        return idx
        
    def waysToSplit(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        l = len(nums)
        s = sum(nums)
        accum = [0]*l
        accum[0] = nums[0]
        for i in range(1,l):
            accum[i] = accum[i-1] + nums[i]
        # use binary search to find 1/3 point
        third = self.binSearch(accum, s // 3)
        tot = 0
        for i in range(third):
            sliced = accum[i+1:]
            half = self.binSearch(sliced, (s - accum[i]) / 2)
            tot += half
        return tot % (10**9 + 7)

sol = Solution()
print(sol.waysToSplit([1,2,2,2,5,0]))