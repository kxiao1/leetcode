# Given string s, first return -1 if it is a palindrome
# Then find any index i such that s is a palindrome with s[i] removed
# If no such i exists, return i again

def palindromeIndex(s):
    # Write your code here
    j = 0
    k = len(s) - 1
    
    while (j <= k):
        if s[j] != s[k]:
            break
        j += 1
        k -= 1
    
    if (j > k):
        return -1 # is a palindrome

    # we must ignore either s[j] or s[k]

    # use new variables to avoid changing j and k
    jj = j + 1
    kk = k
    while (jj <= kk):
        if s[jj] != s[kk]:
            break
        jj += 1
        kk -= 1
    
    if (jj > kk):
        return j # first fix worked
    
    jj = j
    kk = k - 1
    while (jj <= kk):
        if s[jj] != s[kk]:
            break
        jj += 1
        kk -= 1
    
    if (jj > kk):
        return k # second fix worked
    
    return -1 # neither fix worked

print(palindromeIndex("quyjjdcgsvvsgcdjjyq"))
print(palindromeIndex("hgygsvlfwcwnswtuhmyaljkqlqjjqlqkjlaymhutwsnwcflvsgygh"))
print(palindromeIndex("fgnfnidynhxebxxxfmxixhsruldhsaobhlcggchboashdlurshxixmfxxxbexhnydinfngf"))
print(palindromeIndex("bsyhvwfuesumsehmytqioswvpcbxyolapfywdxeacyuruybhbwxjmrrmjxwbhbyuruycaexdwyfpaloyxbcpwsoiqtymhesmuseufwvhysb"))
print(palindromeIndex("fvyqxqxynewuebtcuqdwyetyqqisappmunmnldmkttkmdlnmnumppasiqyteywdquctbeuwenyxqxqyvf"))
print(palindromeIndex("mmbiefhflbeckaecprwfgmqlydfroxrblulpasumubqhhbvlqpixvvxipqlvbhqbumusaplulbrxorfdylqmgfwrpceakceblfhfeibmm"))
print(palindromeIndex("tpqknkmbgasitnwqrqasvolmevkasccsakvemlosaqrqwntisagbmknkqpt"))
print(palindromeIndex("lhrxvssvxrhl"))
print(palindromeIndex("prcoitfiptvcxrvoalqmfpnqyhrubxspplrftomfehbbhefmotfrlppsxburhyqnpfmqlaorxcvtpiftiocrp"))
print(palindromeIndex("kjowoemiduaaxasnqghxbxkiccikxbxhgqnsaxaaudimeowojk"))