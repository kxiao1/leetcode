// https://app.codility.com/programmers/trainings/7/countries_count/
#include <stack>
#include <utility>
#include <vector>

// modified DFS to get connected components
int solution(std::vector<std::vector<int>>& A) {
    int M = A.size(), N = A.front().size();  // size_t causes cast issues later
    std::vector<std::vector<bool>> visited(M, std::vector<bool>(N, false));
    auto in_range = [=](int i, int j) {
        return (i >= 0) && (i < M) && (j >= 0) && (j < N);
    };
    int country_count{0};
    for (int i = 0; i < M; ++i) {
        for (int j = 0; j < N; ++j) {
            if (visited[i][j]) {
                continue;
            }

            ++country_count;

            int curr_color{A[i][j]};
            std::stack<std::pair<int, int>> to_visit;  // adapter has less ctors
            to_visit.push({i, j});
            while (!to_visit.empty()) {
                auto [i, j] = to_visit.top();
                to_visit.pop();

                visited[i][j] = true;
                for (auto [ii, jj] :  // initializer list + template deduction
                     {std::pair(i, j - 1), std::pair(i, j + 1),
                      std::pair(i - 1, j), std::pair(i + 1, j)}) {
                    if (in_range(ii, jj) && !visited[ii][jj] &&
                        curr_color == A[ii][jj]) {
                        to_visit.push({ii, jj});
                    }
                }
            }
        }
    }
    return country_count;
}

int main() {}