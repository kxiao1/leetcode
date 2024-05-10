# https://leetcode.com/problems/min-cost-to-connect-all-points/description/

# solution 1: "Prim"
from heapq import *


def minCostConnectPoints(points):
    """
    :type points: List[List[int]]
    :rtype: int
    """

    n = len(points)
    added = [False] * n
    dists = []  # will become a heap
    tot_cost = 0

    # add first point in
    added[0] = True
    num_added = 1
    curr = 0  # index of first point

    while num_added < n:
        for i, p in enumerate(points):
            if i != curr and not added[i]:
                new_dist = abs(p[0] - points[curr][0]) + abs(p[1] - points[curr][1])
                heappush(dists, (new_dist, i))
        dist, v = heappop(dists)
        while added[v]:
            dist, v = heappop(dists)

        added[v] = True
        num_added += 1
        tot_cost += dist
        curr = v

    return tot_cost


# solution 2: "Kruskal"


def minCostConnectPoints(self, points):
    """
    :type points: List[List[int]]
    :rtype: int
    """

    dists = []
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points[i + 1 :]):
            dists.append((abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]), (i, i + 1 + j)))

    dists.sort(key=lambda x: x[0])
    tot_cost = 0
    num_edges = 0

    # path-compression in find
    def f(reps, p):
        if p != reps[p]:
            reps[p] = f(reps, reps[p])
        return reps[p]

    reps = list(range(len(points)))  # class representatives
    sizes = [1] * len(points)
    for dist, pair in dists:
        # "find"
        r1 = f(reps, pair[0])
        r2 = f(reps, pair[1])

        if r1 != r2:
            # "union"
            if sizes[r2] > sizes[r1]:
                r1, r2 = r2, r1
            sizes[r1] += sizes[r2]
            reps[r2] = r1

            # check if we're done
            tot_cost += dist
            num_edges += 1
            if num_edges == len(points) - 1:
                break

    return tot_cost


points = [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]
points = [[3, 12], [-2, 5], [-4, 1]]
