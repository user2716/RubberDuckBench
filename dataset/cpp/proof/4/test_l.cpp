#include <stdio.h>
#include <sys/time.h>
#include <iostream>

int main() {

    struct timeval tstart, tend;

    gettimeofday(&tstart, NULL);

    for (int i = 0; i < 10000000; i++) {
        std::wstring test = L"";
        std::wcout << test;
    }


    gettimeofday(&tend, NULL);

    double timer = tend.tv_sec - tstart.tv_sec + (tend.tv_usec - tstart.tv_usec)/1.e6;

    printf("time is %g\n", timer);
}



