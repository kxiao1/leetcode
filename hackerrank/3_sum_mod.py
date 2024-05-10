# find number of triples (i, j, k) such that arr[i] + arr[j] + arr[k] is divisible by d
import random


def helper(mods, targetOrig):
    cnt = 0
    # actually no need to optimize the range of the loop (see below)
    for num1 in range(0, min(targetOrig + 1, len(mods))):  # need range(, end + 1)
        if mods[num1] == 0:
            continue
        mods[num1] -= 1

        target2 = targetOrig - num1
        for num2 in range(num1, min(target2 + 1, len(mods))):
            if mods[num2] == 0:
                continue

            choices = {num1: 1}

            choices[num2] = choices.get(num2, 0) + 1
            mods[num2] -= 1

            target3 = target2 - num2
            if target3 >= num2 and target3 < len(mods) and mods[target3] > 0:
                choices[target3] = choices.get(target3, 0) + 1
                print(choices)

                # temporarily return these to original counts for pnc calculation
                mods[num2] += 1
                mods[num1] += 1
                temp = 1
                for (k, v) in choices.items():
                    if v == 1:
                        temp *= mods[k]
                    elif v == 2:
                        temp *= (mods[k] * (mods[k] - 1) / 2)
                    else:  # v == 3
                        temp *= (mods[k] * (mods[k] - 1) * (mods[k] - 2)) / 6
                cnt += temp

                mods[num1] -= 1
                mods[num2] -= 1

            mods[num2] += 1

        mods[num1] += 1
    print("count:", cnt)
    return cnt


def getTripletCount(arr, d):
    # Write your code here
    # print(arr, d)

    mods = [0] * d
    for elem in arr:
        mod = elem % d
        mods[mod] += 1

    cnt = 0

    # case 1: 3 add up to 0
    cnt += helper(mods, 0)

    # case 2: 3 add up to d
    cnt += helper(mods, d)

    # case 3: 3 add up to 2d
    cnt += helper(mods, 2 * d)

    return cnt

# same logic but less code


def getTripletCountFaster(arr, d):
    mods = [0] * d
    for elem in arr:
        mod = elem % d
        mods[mod] += 1

    cnt = 0
    for i in range(len(mods)):
        for j in range(i, len(mods)):
            k = (d - i - j) % d
            
            if k < j: # need this to avoid double-counting
                continue

            choices = dict()
            for c in [i,j,k]:
                choices[c] = choices.get(c, 0) + 1

            temp = 1
            for k, v in choices.items():
                num = mods[k]
                # will implicitly multiply by 0 if num < v
                if v == 1:
                    temp *= num
                elif v == 2:
                    temp *= (num * (num - 1)) // 2
                else:
                    temp *= (num * (num - 1) * (num - 2)) // 6

            cnt += temp
    return cnt

def getTripletCountBrute(arr, d):
    cnt = 0
    for i in range(0, len(arr)):
        for j in range(i + 1, len(arr)):
            for k in range(j + 1, len(arr)):
                if (arr[i] + arr[j] + arr[k]) % d == 0:
                    cnt += 1
    return cnt


l = [9, 32, 24, 8, 7, 12, 10, 11]
d = 3
soln = getTripletCountBrute(l, d)
mysoln = getTripletCount(l, d)
mysolnFast = getTripletCountFaster(l, d)
print(soln, mysoln, mysolnFast)
assert(soln == mysoln == mysolnFast)

l = [58, 62, 81, 41, 19, 2, 38, 43, 91, 96]
d = 37
soln = getTripletCountBrute(l, d)
mysoln = getTripletCount(l, d)
mysolnFast = getTripletCountFaster(l, d)
print(soln, mysoln, mysolnFast)
assert(soln == mysoln == mysolnFast)

num = 100
l = []
for i in range(num):
    l.append(int(random.random() * num * 10))
d = 37
print(l)
soln = getTripletCountBrute(l, d)
mysoln = getTripletCount(l, d)
mysolnFast = getTripletCountFaster(l, d)
print(soln, mysoln, mysolnFast)
assert(soln == mysoln == mysolnFast)
