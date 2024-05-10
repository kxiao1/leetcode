"""
I have 100 records. My device plays 1 per minute, randomly, with replacement. 
How long before it is 50% likely all have been played?

Source:
https://www.facebook.com/groups/1923323131245618/permalink/3908880319356546/

We present an exact solution (inclusion and exclusion) and verify it with a simulation.

Note that we can also use the union bound to derive an upper bound on the number of plays:

P(#1 not played OR #2 not played... OR  #100 not played) <= 100 * P(#i not played) so
P(all played) = 1 - P(#1 not played OR #2 not played... OR  #100 not played) 
            >= 1 - 100 * P(#i not played).
So it is sufficient to pick N large enough such that 
1 - 100 * P(#i not played) >= 0.5
<=> P(#i not played) <= 0.005
<=> 0.99^N <= 0.005
<=> N >= 527.17.. = 528

"""

import matplotlib.pyplot as plt
import numpy as np
from utils.binom import *

rng = np.random.default_rng()


def pick_record():
    return int(rng.random() * 100)


max_plays = 1000


def play_n_records(n: int):
    played = [0] * 100
    num_played = 0  # no. played before we got all 100
    while (sum(played) < 100) and num_played < n:
        played[pick_record()] = 1
        num_played += 1
    if sum(played) < 100:
        num_played += 1  # indicates that we did not get all 100
    return num_played


def calc_prob_n(n: int):
    p = 0
    sign = 1
    for i in range(101):
        p += sign * mCn(100, i) * (1 - i / 100) ** n
        sign *= -1
    return p


def sim():
    num_trials = 10000

    # no. of trials with n plays needed
    pdf = np.zeros(max_plays + 2)  # n ranges from 0... 1001

    for _ in range(num_trials):
        res = play_n_records(max_plays)
        pdf[res] += 1

    cdf = np.cumsum(pdf)[:-1] / num_trials
    x_axis = np.arange(max_plays + 1)
    plt.plot(x_axis, cdf, ":", label="sim")
    return


def calc():
    x_axis = np.arange(max_plays + 1)
    y_axis = np.zeros(max_plays + 1)

    # the formula still works if n < 100 but we get a float overflow
    for n in range(100, max_plays + 1):
        y_axis[n] = calc_prob_n(n)
    plt.plot(x_axis, y_axis, ":", label="calc")
    return


def upper_bound():
    x_axis = np.arange(500, max_plays + 1)
    y_axis = np.empty(max_plays + 1 - 500)

    for n in range(500, max_plays + 1):
        y_axis[n - 500] = 1 - 100 * 0.99**n
    plt.plot(x_axis, y_axis, ":", label="ubound")
    return


sim()
calc()
upper_bound()
plt.legend()
plt.show()
