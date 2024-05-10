#include "tcp_over_udp.h"
/* Two other implementations followed by simple test code*/

// More cumbersome than pq when working exclusively with the smallest element
class MapProcessor : public DataProcessor {
   public:
    MapProcessor(size_t k) : max_size(k) {}

   private:
    std::optional<Packet> getFromBuffer(int nextSeqNum) override {
        // prune the tree
        if ((!bst.empty()) && bst.begin()->first < nextSeqNum) {
            bst.erase(bst.begin(), bst.lower_bound(nextSeqNum));
        }
        if (bst.empty()) {
            return std::optional<Packet>();
        }

        auto& [k, v] = *bst.begin();
        if (k == nextSeqNum) {
            bst.erase(k);
            // can also move/ reset/ exchange etc
            return std::make_optional<Packet>(k, v);
        }
        return std::optional<Packet>();
    }

    bool pushToBuffer(int seqNum, int value) override {
        if (bst.size() < max_size) {
            bst.emplace(seqNum, value);  // equivalent to insert for int value
            return true;
        }
        return false;
    }

    // Override default implementation
    std::optional<Packet> flushBuffer(int nextSeqNum) override {
        if (!flushing) {
            curr_pos = bst.begin();
            flushing = true;
        }
        if (curr_pos == bst.end()) {
            return std::optional<Packet>();
        }
        auto& [k, v] = *curr_pos;
        if (k == nextSeqNum) {
            ++curr_pos;  // no need to erase here since we are flushing
            return std::make_optional<Packet>(k, v);
        }
        return std::optional<Packet>();
    }

    size_t max_size;  // to be initialized
    std::map<int, int> bst;
    std::map<int, int>::iterator curr_pos;
    bool flushing = false;
};

// Limit based on max seq num not size of buffer
class CircularBufferProcessor : public DataProcessor {
   public:
    CircularBufferProcessor(size_t k) : max_size(k) { buffer.resize(k); }

   private:
    std::optional<Packet> getFromBuffer(int nextSeqNum) override {
        // We could check and invalidate all the old data (e.g. keep track of
        // prevSeqNum, and clear min(nextSeqNum - prevSeqNum - 1, max_size) many
        // elements starting from prevSeqNum + 1) Alternatively just lazily
        // invalidate the data like we do here
        this->nextSeqNum = nextSeqNum;
        if (auto opt = buffer[nextSeqNum % max_size]) {
            // if not what we want, don't return but still invalidate
            buffer[nextSeqNum % max_size].reset();
            if (opt->seqNum == nextSeqNum) {
                return opt;
            }
        }
        return std::optional<Packet>();
    }

    bool pushToBuffer(int seqNum, int value) override {
        if ((seqNum - nextSeqNum) < (int)max_size) {
            buffer[seqNum % max_size] =
                std::make_optional<Packet>(seqNum, value);
            return true;
        }
        return false;
    }

    // Override default implementation
    std::optional<Packet> flushBuffer(int nextSeqNum) override {
        if (currIdx < 0) {
            currIdx = nextSeqNum % max_size;
        }
        auto opt = buffer[currIdx];
        if (opt && opt->seqNum == nextSeqNum) {
            currIdx = (currIdx + 1) % max_size;
            return opt;
        }
        return std::optional<Packet>();
    }

    size_t max_size;  // to be initialized
    std::vector<std::optional<Packet>> buffer;
    int nextSeqNum = 1;

    int currIdx = -1;
};

int main() {
    DataProcessor* DP1 = new PriorityQueueProcessor(32);
    DataProcessor* DP2 = new MapProcessor(32);
    DataProcessor* DP3 = new CircularBufferProcessor(32);
    std::vector<int> in{2, 1, 3, 5,  6,  4,  5,  6, 2,
                        7, 3, 8, 10, 12, 13, 11, 9, 15};
    for (DataProcessor* DP : {DP1, DP2, DP3}) {
        for (int v : in) {
            auto [packet, state] = DP->get_next(v, v);
            if (packet) {
                std::cout << packet->seqNum << " ";
            } else {
                std::cout << "<> ";
            }
        }
        std::cout << std::endl;
    }
    for (DataProcessor* DP : {DP1, DP2, DP3}) {
        while (auto packet = DP->flush()) {
            std::cout << packet->seqNum << " ";
        }
        std::cout << std::endl;
    }
};
