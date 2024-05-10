import random

# https://leetcode.com/discuss/interview-question/718692/facebook-training-balanced-split
# Looks like https://leetcode.com/problems/partition-equal-subset-sum/ but DIFFERENT!
# Find if a subset (LEFT) sums to half the total, all LEFT < RIGHT
# The following (quickselect) solution works for this specification, see also cpp


def balancedSplitExists(arr):
    # Write your code here
    s = sum(arr)
    if s % 2 == 1:
        return False
    goal = s // 2
    while True:
        pivot = arr[random.randint(0, len(arr) - 1)]
        lHalf = []
        rHalf = []
        for v in arr:
            if v <= pivot:
                lHalf.append(v)
            else:
                rHalf.append(v)

        lSumPivot = sum(lHalf)

        # key idea: we can't split the elements equal to pivot
        if lSumPivot == goal:
            return True

        if lSumPivot < goal:
            arr = rHalf
            goal -= lSumPivot
            continue

        # if LEFT <= RIGHT is allowed, then we can split the pivot elements
        # so need to decide how to split them. Here our we are just checking if left
        # are all equal to pivot, which is not that efficient (see cpp solution)
        # because we don't reduce arr's size in this case
        if all(i == lHalf[0] for i in lHalf):
            return False  # there's a blob in the middle we can't separate

# These are the tests we use to determine if the solution is correct.
# You can add your own at the bottom.


def printString(string):
    print('[\"', string, '\"]', sep='', end='')


test_case_number = 1


def check(expected, output):
    global test_case_number
    result = False
    if expected == output:
        result = True
    rightTick = '\u2713'
    wrongTick = '\u2717'
    if result:
        print(rightTick, 'Test #', test_case_number, sep='')
    else:
        print(wrongTick, 'Test #', test_case_number,
              ': Expected ', sep='', end='')
        printString(expected)
        print(' Your output: ', end='')
        printString(output)
        print()
    test_case_number += 1


if __name__ == "__main__":
    arr_1 = [1, 3]
    expected_1 = False
    output_1 = balancedSplitExists(arr_1)
    check(expected_1, output_1)

    arr_2 = [4, 4, 4, 4]
    expected_2 = False
    output_2 = balancedSplitExists(arr_2)
    check(expected_2, output_2)

    arr_3 = [2, 1, 2, 5]
    expected_3 = True
    output_3 = balancedSplitExists(arr_3)
    check(expected_3, output_3)

    arr_4 = [1, 5, 7, 1]
    expected_4 = True
    output_4 = balancedSplitExists(arr_4)
    check(expected_4, output_4)

    arr_5 = [3, 6, 3, 4, 4]
    expected_5 = False
    output_5 = balancedSplitExists(arr_5)
    check(expected_5, output_5)

    arr_6 = [5, 7, 8]
    expected_6 = False
    output_6 = balancedSplitExists(arr_6)
    check(expected_6, output_6)

    # Add your own test cases here
