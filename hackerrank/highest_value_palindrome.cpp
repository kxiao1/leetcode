/*
Palindromes are strings that read the same from the left or right, for example
madam or 0110.

You will be given a string representation of a number and a maximum number of
changes you can make. Alter the string, one digit at a time, to create the
string representation of the largest number possible given the limit to the
number of changes. The length of the string may not be altered, so you must
consider 0's left of all higher digits in your tests. For example 0110 is valid,
0011 is not.

Given a string s representing the starting number, and a maximum number of k
changes allowed, create the largest palindromic string of digits possible or the
string
'-1' if it is not possible to create a palindrome under the contstraints.

Examples:
s = '1231', k = 3 => Make 3 replacements to get '9339'
s = '12321', k = 1 => Make 1 replacement to get '12921'
s = '3943', k = 1 => Make 1 replacement to get '3993

n below represents the length of the string.

*/

#include <string>
#include <vector>
// The DP solution will be O(nk)
std::string highestValuePalindromeDP(std::string s, int n, int k) {
    return "-1";
}

// The non-DP solution is strictly linear (O(n))
std::string highestValuePalindrome(std::string s, int n, int k) {
    int i{0}, j{n - 1};
    std::vector<bool> changed(n, false);

    // make the minimum changes needed
    while (i < j) {
        if (s[i] != s[j]) {
            if (s[i] > s[j]) {
                s[j] = s[i];
            } else {
                s[i] = s[j];
            }
            changed[i] = true;
            --k;
        }
        ++i;
        --j;
    }
    if (k < 0) {
        return "-1";
    }

    // from here on, we want to be greedily apply our allowance
    i = 0;
    j = n - 1;
    while (i <= j && k > 0) {
        if (s[i] != '9') {
            if (changed[i] || i == j) {
                --k;                // just need to change the other number
                changed[i] = true;  // note edge case: odd palindrome
                s[i] = '9';
                s[j] = '9';
            }
            if (!changed[i] && k > 1) {  // I hate else if without else
                k -= 2;                  // need to change both
                s[i] = '9';
                s[j] = '9';
            }
        }
        ++i;
        --j;
    }
    return s;
}