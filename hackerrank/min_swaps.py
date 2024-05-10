# given an array, return the minimum swaps need to sort it

# arr: array to sort
def solution(arr):
    ref = list(enumerate(arr))
    ref.sort(key=lambda x: x[1])

    visited = set()
    res = 0

    for (idx, val) in enumerate(arr):
        if ref[idx][1] == val or idx in visited:  # correct position
            continue

        cycleLen = 0
        i = ref[idx][0]
        v = arr[i]
        while i != idx:
            visited.add(i)
            i = ref[i][0]
            v = arr[i]
            cycleLen += 1
        res += cycleLen
    return res


test1 = [[2, 4, 5, 1, 3], 3]
test2 = [[1, 3, 5, 2, 4, 6, 7], 3]
tests = [test1, test2]

for test in tests:
    res = solution(test[0])
    ans = test[1]
    if res != ans:
        print("Expected:", ans, "Actual", res)
    else:
        print("PASS")
