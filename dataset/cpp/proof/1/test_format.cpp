// install: sudo apt install libfmt-dev
// build: g++ test_format.cpp -lfmt

#include <stdio.h>
#include <sys/time.h>
#include <iostream>
#include <fmt/core.h>

std::string fn(std::string g) {

    std::string s = "";
    s.reserve((g.size() + 1) * 100);
    for (int i = 0; i < 100; i++) {
        s += g;
        s.push_back(' ');
    }

    return s;
}


int main(int argc, char* argv[]) {

    struct timeval tstart, tend;

    double timer;
    const char * str = fn(argv[2]).c_str();

    gettimeofday(&tstart, NULL);

    for (int i = 0; i < 10000000; i++) {
        std::string test = fmt::format("[{}] {} ", fn(argv[1]), std::string(str, 0));
    }

    gettimeofday(&tend, NULL);

    timer = tend.tv_sec - tstart.tv_sec + (tend.tv_usec - tstart.tv_usec)/1.e6;

    printf("time is %g\n", timer);

}
