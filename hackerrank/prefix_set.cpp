#include <iostream>
#include <set>
#include <string>
#include <vector>
using namespace std;

/*
 * words is prefix-free and "GOOD" iff there are no prefix pairs (e.g. AB, ABB).
 *
 * The main idea is that IF there are prefix pairs in words, then the FIRST time
 * it occurs, the pair of words will be adjacent.
 */

void noPrefix(vector<string> words) {
    set<string> dict;
    for (const auto& word : words) {
        auto it = dict.lower_bound(word);

        // case 1: another word is the prefix of this word
        if (it != dict.begin() && word.find(*prev(it)) == 0) {
            cout << "BAD SET\n" << word << endl;
            return;
        }

        // case 2: this word is the prefix of another word
        if (it != dict.end() && it->find(word) == 0) {
            cout << "BAD SET\n" << word << endl;
            return;
        }

        dict.emplace(word);
    }
    cout << "GOOD SET" << endl;
}

// 2nd solution
void noPrefix2(vector<string> words) {
    set<string> dict;  // dictionary of words
    for (const auto& word : words) {
        // case 1: another word is the prefix of this word
        for (size_t i = 1; i <= word.size(); ++i) {
            // or dict.contains (C++20)
            if (dict.count(word.substr(0, i))) {
                cout << "BAD SET\n" << word << endl;
                return;
            }
        }

        // case 2: this word is the prefix of another word
        auto it = dict.lower_bound(word);
        if (it != dict.end() && it->find(word) == 0) {
            cout << "BAD SET\n" << word << endl;
            return;
        }

        dict.insert(word);
    }
    cout << "GOOD SET" << endl;
}