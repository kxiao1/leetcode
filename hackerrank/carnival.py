# Given the starting positions of cities on a map, and their populations, find
# the optimal location to host a carnival by minimizing the total Manhattan
# distance travelled. Return this distance.

# len(pops) = len(xcoords) = len(ycoords)
def solution(pops, xcoords, ycoords):
    maxX = max(xcoords)
    maxY = max(ycoords)
    matrix = [[0] * (maxY + 1) for x in range(maxX + 1)]

    xdisps = [-1, 0, 1]
    ydisps = [-1, 0, 1]
    for (idx, pop) in enumerate(pops):
        startX = xcoords[idx]
        startY = ycoords[idx]
        for x in range(0, maxX + 1):
            for y in range(0, maxY + 1):
                cost = pop * (abs(x-startX) + abs(y-startY))
                matrix[x][y] += cost
    rowMin = [min(row) for row in matrix]
    return min(rowMin)


test1 = [[1, 1], [1, 3], [1, 1], 2]  # pops, xcoords, ycoords, expected answer
test2 = [[1, 1], [1, 2], [1, 2], 2]
test3 = [[1,1,1], [4, 1, 3], [1, 5, 8], 10]
test4 = [[1,1,1], [5, 1, 3], [1, 5, 8], 11]
tests = [test1, test2, test3, test4]

for test in tests:
    res = solution(test[0], test[1], test[2])
    ans = test[3]
    if res != ans:
        print("Expected:", ans, "Actual", res)
    else:
        print("PASS")
