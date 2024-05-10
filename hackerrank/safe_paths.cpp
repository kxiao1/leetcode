#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;
/*
* each journey in journeys has the form "x y k", all underlying ints 
* (x,y) represents the ending coordinates
* a valid path to (x,y) has the form "[VH]*", representing vertical and 
* horizontal steps respectively 
* k is the index in the lexicographically sorted list of paths to (x,y)
* that represents the safe path. for each journey, we want list[k]
* Return: the list of safe paths for the list of journeys
*/


/* The prompt specifies the following "algorithm":
"Begin by creating all possible paths from the origin to the target location
represented as strings of H and V. Order the strings lexicographically
ascending..." but top-down DP is probably faster
https://leetcode.com/discuss/interview-question/527769/lucid-oa-gridland
*/

vector<string> getSafePaths(vector<string> journeys) {
  string space = " ";
  vector<string> res;
  vector<int> xs;
  vector<int> ys;
  vector<int> keys;
  for (auto journey : journeys) {
    int ix = journey.find(" ");
    int x = stoi(journey.substr(0, ix));
    xs.push_back(x);
    auto rest = journey.substr(ix + 1);
    int iy = rest.find(" ");
    int y = stoi(rest.substr(0, iy));
    ys.push_back(y);
    rest = rest.substr(iy + 1);
    int key = stoi(rest);
    keys.push_back(key);
  }
  int x = *max_element(xs.begin(), xs.end());
  int y = *max_element(ys.begin(), ys.end());
  vector<vector<unordered_set<string>>> allPaths(
      x + 1, vector<unordered_set<string>>(y + 1, unordered_set<string>()));

  allPaths[0][0].insert("");

  // TODO: this part is buggy
  // using an unordered set doesn't preserve the order of paths
  // also, maybe lazy top-down DP is better than constructing the entire grid
  for (int i = 0; i < allPaths.size(); ++i) {
    for (int j = 0; j < allPaths[i].size(); ++j) {
      unordered_set<string> n = allPaths[i][j];
      if (i > 0) {
        auto prev = allPaths[i - 1][j];
        for (auto str : prev) {
          n.insert("H" + str); // we always insert the most significant bit so far
        }
      }
      if (j > 0) {
        auto prev = allPaths[i][j - 1];
        for (auto str : prev) {
          n.insert("V" + str);
        }
      }
      allPaths[i][j] = n;
    }
  }

  for (int i = 0; i < xs.size(); ++i) {
    int x = xs[i];
    int y = ys[i];
    int key = keys[i];
    unordered_set<string> fin = allPaths[x][y]; // set of all paths to (x,y)
    vector<string> f(fin.begin(), fin.end()); // might need a sort/ reverse here
    cout << f.size() << key << endl;
    res.push_back(f[key]);
  }
  return res;
}
