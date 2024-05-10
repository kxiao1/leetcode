#
# Complete the 'getServerIndex' function below.
#
# Given n servers, a list of arrival times and service (burst) times of 
# requests, return the server used to serve each request, or -1 if all are busy.
# Note that the index of arrival times might not be in chronological order,
# and if two requests come at the same time, the lower index gets priority. 

# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER_ARRAY arrival
#  3. INTEGER_ARRAY burstTime
#

def getServerIndex(n, arrival, burstTime):
    # Write your code here
    
    l = []
    for i in range(len(arrival)):
        l.append([arrival[i], burstTime[i], i])
    l.sort(key=lambda x: (x[0], x[2]))
    print(arrival, burstTime)
     
    serverWait = [0] * n
    prevTime = 0
    serverAssigned = [0] * len(l)

    for reqTime, totTime, orig_idx in l:
        timeElapsed = reqTime - prevTime
        serverWait = [max(x - timeElapsed, 0) for x in serverWait]

        serverIdx = 0
        while serverIdx < n and serverWait[serverIdx] > 0:
            serverIdx += 1 # go to next server
        
        # all servers busy
        if serverIdx == n:
            serverAssigned[orig_idx] = -1 # assign to the original arrival index
            continue
        
        serverAssigned[orig_idx] = serverIdx + 1 # convert back to 1-indexing
        serverWait[serverIdx] = totTime
        prevTime = reqTime
    
    return serverAssigned

# testing code
arrival = [3, 5, 1, 6, 8]
burstTime = [9, 2, 10, 4, 5]
n = 4

assert(getServerIndex(n, arrival, burstTime) == [2, 3, 1, 4, 3])