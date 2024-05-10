// https://app.codility.com/programmers/trainings/9/sparse_binary_decomposition/
#include <iostream>
#include <ranges>
#include <vector>

/* To get a sparse factor of the decomposition, we can start reading from the
 * most significant bit and include every other bit. */
int solution(int N) {
    std::vector<bool> bin;
    while (N > 0) {
        bin.push_back(static_cast<bool>(N & 1));
        N >>= 1;
    }

    bool add{true};  // whether to read the current bit
    int out{0};
    for (bool b : std::ranges::reverse_view(bin)) {
        out <<= 1;
        if (add) {
            out += static_cast<int>(b);
        }
        add = !add;
    }
    return out;
}
int main() { std::cout << solution(41) << std::endl; }