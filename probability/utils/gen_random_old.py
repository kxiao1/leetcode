import random
import sys

"""
Manual way of generating permutations - np.permutation is preferred
"""


def permute(arr):
    if len(arr) == 1:
        return arr
    idx = int(random.random() * len(arr))
    first = arr[idx]
    arr[idx] = arr[0]
    arr[0] = first
    res = permute(arr[1:])
    res.append(first)
    return res


# N: returns random permutation of [0, 1,2,...N-1]
def gen_random(N):
    return permute(list(range(N)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "usage: python gen_random.py N M\n \
        N = size of array\n \
        M = number of random arrays"
        )
    else:
        for i in range(int(sys.argv[2])):
            print(gen_random(int(sys.argv[1])))
