class Lollipop {
   public:
    // total_size >= loop_size >= 0
    Lollipop(int total_size, int loop_size);

    // move constructor and assignment
    Lollipop(Lollipop &&other);
    Lollipop &operator=(Lollipop &&other);

    // delete copy constructor and assignment
    Lollipop(const Lollipop &other) = delete;
    Lollipop &operator=(const Lollipop &other) = delete;

    // destructor
    ~Lollipop();

    void *head();
    void *move(void *ptr);
    void make_next(void *curr, void *next);

   private:
    void **list;
};
