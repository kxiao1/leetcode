# quick script to calculate P(AB or BC or CD) i.e. prob_straight3 in poker_probs.py. Credit:
# https://math.stackexchange.com/questions/3624102/probability-of-getting-two-specific-cards-in-7-card-poker-hand-using-ordinary-d
set.seed(1234)
deck = c(rep(1,4),rep(10,4),rep(100,4),rep(1000,4),rep(0, 48-16))
tot = replicate(10^7, sum(sample(deck,7)))
mean(pmax((tot%%10 >= 1) * (tot %% 100 >= 10),  # has 1 and 10
    (tot %% 100 >= 10) * (tot %% 1000 >= 100),    # has 10 and 100
    (tot %% 1000 >= 100) * (tot %% 10000 >= 1000))) # has 100 and 1000