def calculateNonnegativeRoot(y):
    # Binary search for the root, starting from the upper bound of max(y,1)
    # print(y)
    top = max(y,1)
    bot = 0
    while abs(top - bot) >= 0.01:
        mid = (top + bot) / 2
        if mid**4 + mid**2 - y > 0:
            top = mid
        else:
            bot = mid
    # correct answer: if top**4 + top **2 - y overshoots, use bot
    print(top,bot)
    guess = int(100*top) / 100
    if guess**4 + guess**2 - y > 0:
        return int(100*bot)
    return int(100*top)

print(calculateNonnegativeRoot(1000000000))
print(calculateNonnegativeRoot(160400))