#include <system_error>
#include <memory>

#ifndef TWO_H
#define TWO_H


void handleConnectException(
        struct addrinfo** nextAddr,
        int error_code,
        bool* anyRefused,
        bool* anyReset,
        bool wait);

void handleConnectSystemError(
        struct addrinfo** nextAddr,
        std::system_error& e,
        bool* anyRefused,
        bool* anyReset,
        bool wait);

int connect(addrinfo** address,
        std::shared_ptr<struct ::addrinfo> addresses,
        bool wait);

#endif
