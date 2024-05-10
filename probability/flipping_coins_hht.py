import random

numTrials = 100000
HTTs = 0
Counts = 0

'''
We toss coins until either HHT or HTT is obtained. Print
1) probability of ending with HHT
2) the expected number of coin tosses
There are better solutions using Markov chains or OST.
'''
for i in range(numTrials):
    seq = ""
    count = 0
    while (seq[-3:] != "HTT") and (seq [-3:] != "HHT"):
        if random.random() < 0.5:
            seq += "H"
        else:
            seq += "T"
        count += 1
    Counts += count
    if seq[-3:] == "HHT":
        HTTs += 1

print(HTTs / numTrials) # should be ~ 2/3
print(Counts / numTrials) # ahouls be ~ 16/3


