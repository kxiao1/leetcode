# sieve of eratosthenes
def first_q_primes(q):
    gens = [2]
    gensIdx = [1]
    prev = 2  # we use primes up to prev to eliminate composites
    curr = 4  # we have found all primes up to curr
    
    composites = set()  # use set because we don't know the range to check (~nlogn)
    
    while len(gens) < q:
        # iterate through all primes up to prev
        for i, gen in enumerate(gens): 
            while gen * gensIdx[i] <= curr:
                composites.add(gen * gensIdx[i])
                gensIdx[i] += 1
        
        # find all primes up to curr = prev ** 2
        for i in range(prev + 1, curr + 1):
            if i not in composites:
                gens.append(i)
                gensIdx.append(1 + (curr // i))  # start after curr
                
        prev = curr
        curr = prev * prev

    return gens[:q]

# go for this during interviews
def simple_primes(q):
    primes = [2]
    n = 3
    
    while len(primes) < q:
        cand = 2
        while cand * cand <= n and n % cand > 0:
            cand += 1
        if n % cand > 0:  # cannot check latter if we start from n = 2
            primes.append(n)
        n += 2  # small optimization to only check odd numbers
    
    return primes