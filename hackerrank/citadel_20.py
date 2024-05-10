# Given an array d, find the number of ordered pairs (a,b,c) such that 
# d[a] < d[b] < d[c] and d[a] + d[b] + d[c] <= t

import time
# Return the largest index low <= i <= high such that l[i] <= v,
# Return low - 1 if all l[i] > v, return -1 if low > high



def binSearch(l, v, low, high):
    if low > high:
        return -1
    mid = 0  # assign later
    while low <= high:
        mid = (low + high) // 2
        if l[mid] == v:
            while mid < len(l) and l[mid] == v: # TODO: use dupTable
                mid += 1
            return mid - 1
        if l[mid] > v:
            high = mid - 1
        else:
            low = mid + 1
    return low - 1

# Binary search but O(n^2logn) because the range [nextStart, nextEnd] 
# is still traversed linearly


def triplets(d, t):
    count = 0
    d.sort()
    for i in range(len(d) - 2):
        nextStart = i
        while nextStart < len(d) - 1 and d[nextStart] == d[i]:
            nextStart += 1  # cannot have same value
        if nextStart >= len(d) - 1:
            break
        nextEnd = binSearch(d, t - d[i], nextStart, len(d) - 2)
        if nextEnd == -1:
            break
        for j in range(nextStart, nextEnd + 1):
            lastStart = j
            while lastStart < len(d) and d[lastStart] == d[j]:
                lastStart += 1
            if lastStart == len(d):
                break
            lastEnd = binSearch(d, t - d[i] - d[j], lastStart, len(d) - 1)
            if lastEnd > -1:
                count += lastEnd - lastStart + 1
    return count


def triplets2(d, t):
    count = 0

    d.sort()
    dupTable = dict()
    for idx, key in enumerate(d):
        dupTable[key] = idx

    for i in range(len(d) - 2):
        nextStart = dupTable[d[i]] + 1
        if nextStart >= len(d) - 1:
            break
        j = nextStart
        while j < len(d) - 1 and d[j] <= t - d[i]:  # linear is fine here
            lastStart = dupTable[d[j]] + 1
            if lastStart == len(d):
                break
            lastEnd = binSearch(d, t - d[i] - d[j], lastStart, len(d) - 1)
            if lastEnd > -1:
                count += lastEnd - lastStart + 1
                j += 1
            else:
                break
    return count

# O(n^2): loop for first val, two-pointers to get other two (no binary search)
def triplets3(d, t):
    count = 0 # will return this

    d.sort()
    dupTable = dict()
    for idx, key in enumerate(d):
        if key in dupTable.keys():
            curr = dupTable[key]
            dupTable[key] = (curr[0], idx) # (startidx for key, endidx for key)
        else:
            dupTable[key] = (idx, idx)
    
    for i in range(len(d) - 2):
        nextStart = dupTable[d[i]][1] + 1
        if nextStart >= len(d) - 1:
            break
        j = nextStart
        k = len(d) - 1
        tot = t - d[i]
        while j < k and d[k] > d[j]:
            # one of the next two while loops will be run
            while k > j and d[j] + d[k] > tot and d[k] > d[j]:
                k = dupTable[d[k]][0] - 1
            while j < k and d[j] + d[k] <= tot and d[k] > d[j]:
                j = dupTable[d[j]][1] + 1
            count += (j - nextStart) * (dupTable[d[k]][1] - dupTable[d[k]][0] + 1)
        assert(j == k or d[j] == d[k])
        j -= 1
        if 2* d[j] <= tot:
            # any 2 from [nextStart, j], account for choosing same num twice
            diff = (j - nextStart + 1) * (j - nextStart) // 2 
            curr = nextStart
            while curr < j:
                temp = dupTable[d[curr]][1] - dupTable[d[curr]][0] + 1
                dupCount = temp * (temp - 1) // 2
                diff -= dupCount
                curr = dupTable[d[curr]][1] + 1
            count += diff 
    return count

def test(d, t, soln = -1):
    # print("TEST", d, t)
    d2 = d[:]
    d.sort()
    if soln == -1:
        soln = 0
        for i in range(len(d) - 2):
            for j in range(i + 1, len(d) - 1):
                for k in range(j + 1, len(d)):
                    if d[i] < d[j] and d[j] < d[k] and d[i] + d[j] + d[k] <= t:
                        soln += 1

    def isCorrect(x): return x == soln

    start = time.time()
    ans = triplets3(d2, t)

    if isCorrect(ans):
        print("PASS: Correct solution %s obtained" % soln)
    else:
        print("FAIL: Expected %s, Got %s" % (soln, ans))
    print("\tTime taken:", time.time() - start)

test([1, 2, 3, 4, 6], 8)
test([1, 2, 4, 4, 4, 4, 6], 7)
test([1, 2, 2, 3, 3, 4, 4, 5, 6], 8)
test([8, 12, 2, 15, 2, 1, 7, 5, 1, 6, 9, 9, 13, 14, 3, 6, 10, 10, 11, 1], 26)
test([4]*10000000, 8, 0)
