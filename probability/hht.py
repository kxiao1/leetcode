import random

numTrials = 500000
HTTs = 0
Counts = 0

"""
We toss coins until either HHT or HTT is obtained. Print
1) probability of ending with HHT
2) the expected number of coin tosses
There are better solutions using Markov chains or OST.
"""
for i in range(numTrials):
    seq = ""
    while (seq[-3:] != "HTT") and (seq[-3:] != "HHT"):
        seq += "H" if random.random() < 0.5 else "T"
        Counts += 1
    if seq[-3:] == "HHT":
        HTTs += 1

print(HTTs / numTrials)  # should be ~ 2/3
print(Counts / numTrials)  # should be ~ 16/3
