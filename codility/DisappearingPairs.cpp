// https://app.codility.com/programmers/trainings/4/disappearing_pairs/
#include <algorithm>
#include <stack>
#include <string>

// Greedily store starts to palindromes, popping once the matching char appears
std::string solution(std::string &S) {
    std::stack<char> store;
    for (char c : S) {
        if (!store.empty() && store.top() == c) {
            store.pop();
        } else {
            store.push(c);
        }
    }
    std::string out(store.size(), ' ');

    for (int i = store.size() - 1; !store.empty(); --i) {
        out[i] = store.top();
        store.pop();
    }
    return out;
}