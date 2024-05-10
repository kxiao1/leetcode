# https://leetcode.com/problems/shortest-word-distance/
# https://aaronice.gitbook.io/lintcode/hash-table/shortest-word-distance

# words: list of str, word1: str, word2: str
# return the shortest distance between any occurrence of word1 and word2 in words
def shortestDistance(words, word1, word2):
    idx1 = []
    idx2 = []
    m = len(words)
    for i in range(m):
        if words[i] == word1:
            idx1.append(i)
        if words[i] == word2:
            idx2.append(i)
    i1 = i2 = 0
    while i1 < len(idx1) and i2 < len(idx2):
        if idx2[i2] > idx1[i1]:
            while i1 < len(idx1) and idx1[i1] < idx2[i2]:
                i1 += 1
            i1 -= 1 # go 1 back to get the last word1 before idx2[i2]
            m = min(abs(idx2[i2] - idx1[i1]),m)
            i1 +=1 # now advance again
        else:
            while i2 < len(idx2) and idx2[i2] < idx1[i1]:
                i2 += 1
            i2 -= 1
            m = min(abs(idx2[i2] - idx1[i1]),m)
            i2 += 1
    return m


def test(words, word1, word2, expected):
    actual = shortestDistance(words, word1, word2)
    assert actual == expected, "Expected: " + expected + ", Actual: " + actual
    print("test passed")

test(list("aaaccbbb"),"a","b",3)
test(list("aaacccbbcacb"),"a","b",2)
test(list("aaacccbbcccccab"),"a","b",1)

