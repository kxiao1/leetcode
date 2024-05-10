#include <iostream>
#include <map>
#include <optional>
#include <queue>  // for priority queues
#include <vector>

// Given two identical UDP streams, implement a buffered in-order output stream
// Buffer size k can be interpreted as
// 1) number of elements in the buffer <= k, or
// 2) maxSeqNum <= nextSeqNum + k
// TODO: Detect when both copies of the data are missing

// State of packet:
// OLD = an old packet that we already processed,
// CURR = the current packet (seq num = nextSeqNum),
// CACHE = a future packet to be sent out which we keep in buffer
// DISCARD = a future packet we want to keep but the buffer is full
enum STATE { OLD, CURR, CACHE, DISCARD };

// Output Packets
struct Packet {
    int seqNum, value;

    // either use this or compare outside the class
    // bool operator<(const Packet& Other) const {
    //     return seqNum > Other.seqNum; // for a min-heap!!
    // }
};

auto cmp_min_heap = [](const Packet& p1, const Packet& p2) {
    return p1.seqNum > p2.seqNum;
};

// Return information about the next packet in the sequence if possible and the
// last packet
using ResultType = std::pair<std::optional<Packet>, STATE>;

class DataProcessor {
   public:
    // Get out-of-order data from producer and pushes in-order data to consumer
    ResultType get_next(int seqNum, int value) {
        if (seqNum == nextSeqNum) {
            ++nextSeqNum;
            return {std::make_optional<Packet>(seqNum, value), STATE::CURR};
        }

        std::optional<Packet> res = getFromBuffer(nextSeqNum);
        if (res) {
            ++nextSeqNum;
        }
        STATE s = STATE::OLD;  // corresponds to seqNum < nextSeqNum
        if (seqNum >= nextSeqNum) {
            s = pushToBuffer(seqNum, value) ? STATE::CACHE : STATE::DISCARD;
        }
        return {res, s};
    }

    std::optional<Packet> flush() {
        return flushBuffer(nextSeqNum++);  // get then increment
    };

   private:
    // Cleans any stale data before returning a packet corresponding to
    // nextSeqNum
    virtual std::optional<Packet> getFromBuffer(int nextSeqNum) = 0;

    // Adds out-of-order packets to the buffer
    virtual bool pushToBuffer(int seqNum, int value) = 0;

    // Returns the remaining packets in the buffer that are next in line
    virtual std::optional<Packet> flushBuffer(int nextSeqNum) {
        return getFromBuffer(nextSeqNum);
    }

    int nextSeqNum = 1;
};

// "Cleanest implementation"
class PriorityQueueProcessor : public DataProcessor {
   public:
    PriorityQueueProcessor(size_t k) : max_size(k) {}

   private:
    std::optional<Packet> getFromBuffer(int nextSeqNum) override {
        while ((!pq.empty()) && pq.top().seqNum < nextSeqNum) {
            pq.pop();
        }
        if (pq.empty() || pq.top().seqNum > nextSeqNum) {
            return std::optional<Packet>();
        }
        std::optional<Packet> out(pq.top());
        pq.pop();
        return out;
    }

    bool pushToBuffer(int seqNum, int value) override {
        if (pq.size() < max_size) {
            pq.push(Packet{seqNum, value});
            return true;
        }
        return false;
    }

    size_t max_size;  // to be initialized
    std::priority_queue<Packet, std::vector<Packet>, decltype(cmp_min_heap)> pq;
};