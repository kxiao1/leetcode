import numpy as np
import random
import time
import re

from matplotlib import pyplot as plt

# S1 and S2 are the two patterns we will analyze

# A Martingale Approach to the Study of Occurrence of Sequence Patterns in Repeated Experiments (Li 1980)
# S1 happens first with probability 9/14, yet E(tau_1) = 20 > 18 = E(tau_2)
# S1 = "HTHT"
# S2 = "THTT"

# Sanity check based on hht.py
# S1 = "HHT"
# S2 = "HTT"


S1 = "HHHHHH"
S2 = "HTTHHT"

assert len(S1) == len(S2)
NUM_TRIALS = 30000
MAX_LEN = 10 ** (len(S1) // 2)


expected_one = 2 ** len(S1) + len(S1) - 1

# for fun
# expected_two += 2 ** len(S1)


def create_array():
    return np.zeros(MAX_LEN + 1, dtype=int)


tau1s = create_array()
tau2s = create_array()

total_s1s = create_array()
total_s2s = create_array()

S1_wins = create_array()
S2_wins = create_array()
total_done = 0

start_time = time.perf_counter()
for i in range(NUM_TRIALS):
    seq = ""
    num_rounds = 0
    done1 = done2 = False

    while (num_rounds < expected_one) or ((num_rounds < MAX_LEN) and not (done1 and done2)):
        num_rounds += 1
        seq += "H" if random.random() < 0.5 else "T"
        if (not done1) and seq[-len(S1) :] == S1:
            tau1s[num_rounds] += 1
            done1 = True
            if not done2:
                S1_wins[num_rounds] += 1
        if (not done2) and seq[-len(S2) :] == S2:
            tau2s[num_rounds] += 1
            done2 = True
            if not done1:
                S2_wins[num_rounds] += 1

    assert len(seq) >= expected_one
    total_s1 = len(re.findall(f"(?={S1})", seq[:expected_one]))
    total_s2 = len(re.findall(f"(?={S2})", seq[:expected_one]))

    total_s1s[total_s1] += 1
    total_s2s[total_s2] += 1

    # pad the tail
    # if not done1:
    #     tau1s[MAX_LEN] += 1
    # if not done2:
    #     tau2s[MAX_LEN] += 1

    if done1 or done2:
        total_done += 1

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

print("Sample size", total_done, f"P({S1} appears first)=", np.sum(S1_wins) / total_done)
print("Num wins", np.sum(S1_wins), np.sum(S2_wins))
assert np.sum(S1_wins) + np.sum(S2_wins) == total_done

print("Num done", sum(tau1s), sum(tau2s))
assert sum(tau1s) > 0.99 * NUM_TRIALS and sum(tau2s) > 0.99 * NUM_TRIALS

times = np.arange(MAX_LEN + 1)
pdf1 = tau1s / NUM_TRIALS
pdf2 = tau2s / NUM_TRIALS

print("E(tau_1)", np.average(times, weights=pdf1))
print("E(tau_2)", np.average(times, weights=pdf2))

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.plot(pdf1, label=S1)
ax1.plot(pdf2, label=S2)
ax1.set_xlabel("T")
ax1.legend()
ax1.set_title(r"PDF of $\tau$")

cdf1 = np.cumsum(pdf1)
cdf2 = np.cumsum(pdf2)
ax2.plot(cdf1, label=S1)
ax2.plot(cdf2, label=S2)
ax2.set_xlabel("T")
ax2.legend()
ax2.set_title(r"CDF of $\tau$")

exp1 = np.average(times, weights=total_s1s / NUM_TRIALS)
exp2 = np.average(times, weights=total_s2s / NUM_TRIALS)
print(f"EV_{S1} = {exp1:.2f}, EV_{S2} = {exp2:.2f} at T={expected_one}")

NUM_OCC_MAX = 10
WIDTH_OCC = 0.3
nums = np.arange(NUM_OCC_MAX)

ax3.bar(nums, total_s1s[:NUM_OCC_MAX] / NUM_TRIALS, WIDTH_OCC, label=S1)
ax3.bar(nums + WIDTH_OCC, total_s2s[:NUM_OCC_MAX] / NUM_TRIALS, WIDTH_OCC, label=S2)
ax3.set_xlabel("k")
ax3.legend()
ax3.set_title(f"P(#{S1}=k) and P(#{S2}=k) at T={expected_one}")

NUM_ROUND_MAX = MAX_LEN // 2 + 1
WIDTH_ROUND = NUM_ROUND_MAX / 40
num_rounds = np.arange(NUM_ROUND_MAX)
S1_hist, bin1 = np.histogram(num_rounds, weights=S1_wins[:NUM_ROUND_MAX])
S2_hist, bin2 = np.histogram(num_rounds, weights=S2_wins[:NUM_ROUND_MAX])
print(sum(S1_hist), S1_hist, bin1)
print(sum(S2_hist), S2_hist, bin2)

ax4.bar(bin1[:-1], S1_hist, WIDTH_ROUND, label=S1)
ax4.bar(bin2[:-1] + WIDTH_ROUND, S2_hist, WIDTH_ROUND, label=S2)
ax4.set_xlabel("Round #")
ax4.legend()
ax4.set_title(f"Winning turns for {S1} and {S2} at T={expected_one}, EV = {exp2:.2f}")
plt.show()
