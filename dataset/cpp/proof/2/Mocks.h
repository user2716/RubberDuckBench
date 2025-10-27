#ifndef MOCKS_H
#define MOCKS_H

struct addrinfo {
    char *ai_addr;	
    struct addrinfo *ai_next;
    int seed;
};

namespace mock {
    int connect(int socket, const addrinfo& addr, int* error_code);
    int poll(int* error_code);
    void getsockopt(int socket, int* error_code);
}

#endif
