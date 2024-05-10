'''
Find sentences that contain all words in a query

input: sentences, queries
output: 2d list, one list for each query
        In each list, for each sentence that contains all words, 
        include the sentence index n times where n is the min of 
        the number of times each word appears. If no sentence
        contains all words, the list is [-1]

NOTE: we assume the words are sparsely distributed: each word
will appear in at most k sentences for k small

NOTE: the important thing is mapping words to sentences instead
of sentences to words, however tempting that might be

'''
def textQueries(sentences, queries):
    # freqs maps words to sentences to counts

    freqs = dict()
    for (i, sentence) in enumerate(sentences):
        for word in sentence.split():
            if word not in freqs:
                freqs[word] = dict()
            if i not in freqs[word]:
                freqs[word][i] = 0
            freqs[word][i] += 1
    
    resList = []
    for query in queries:
        s = None
        for word in query.split(): 
            if s is None:
                s = set(freqs[word].keys())
            else:
                s = s.intersection(set(freqs[word].keys()))
        if len(s) == 0:
            resList.append([-1])
            continue

        l = sorted(list(s))
        res = []
        for idx in l:
            min_cnt = 10
            for word in query.split():
                min_cnt = min(min_cnt, freqs[word][idx])
            for _ in range(min_cnt):
                res.append(idx)
        resList.append(res)
    
    return resList

# [2], [0, 1, 1, 2]]
print(textQueries(['jim likes mary','kate likes tom likes', 'tom does not like that jim likes kate'],['jim tom', 'likes']))
