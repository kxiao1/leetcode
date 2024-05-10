# https://www.hackerrank.com/challenges/truck-tour/problem

def truckTour(petrolpumps):
    # Write your code here
    cumul = 0
    trough = 0
    troughIdx = -1
    for i in range(len(petrolpumps)):
        cumul += petrolpumps[i][0] - petrolpumps[i][1]
        if cumul < trough:
            trough = cumul
            troughIdx = i
    return troughIdx + 1

def truckTourSlow(petrolpumps):
    # Write your code here
    startIdx = 0
    cumulNet = [petrolpumps[0][0] - petrolpumps[0][1]]
    for i in range(1, len(petrolpumps)):
        cumulNet.append(cumulNet[-1] + petrolpumps[i][0] - petrolpumps[i][1])
    troughs = [cumulNet[-1]]
    for i in range(1, len(cumulNet)):
        troughs.append(min(cumulNet[(-i) - 1], troughs[-1]))
    troughs.reverse()
    # print(troughs)
    
    trough2 = troughs[0]
    trough1 = 0
    while trough1 < 0 or trough2 < 0:
        startIdx += 1
        trough2 = troughs[startIdx] - cumulNet[startIdx - 1]
        trough1 = troughs[startIdx - 1] + cumulNet[-1] - cumulNet[startIdx-1]
    return startIdx