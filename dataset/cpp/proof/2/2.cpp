#include <iostream>
#include <memory>
#include "errno.h"
#include "Mocks.h"

using namespace std;
//using namespace mock;


void handleConnectException(
        shared_ptr<struct addrinfo> addresses,
        struct addrinfo** nextAddr,
        int error_code,
        bool* anyRefused,
        bool* anyReset,
        bool wait) {

    // ECONNREFUSED happens if the server is not yet listening.
    if (error_code == ECONNREFUSED) {
        cout << "\t encountered ECONNREFUSED" << endl;
        *anyRefused = true;
    }
    // ECONNRESET happens if the server's listen backlog is exhausted.
    if (error_code == ECONNRESET) {
        *anyReset = true;
    }

    if (error_code != ECONNRESET && error_code != ECONNREFUSED) {
        std::cout << "\tEncountered an error code other than RESET or REFUSED: " << error_code << std::endl;
    }

    // We need to move to the next address because this was not available
    // to connect or to create a socket.
    *nextAddr = (*nextAddr)->ai_next;

    // We have tried all addresses but could not connect to any of them.
    if (!*nextAddr) {
        if (!wait || (!*anyRefused && !*anyReset)) {
            std::cout << "Done trying connections" << std::endl;
            throw;
        }

        *anyRefused = false;
        *anyReset = false;
        *nextAddr = addresses.get(); //back to beginning
    }
}

void handleConnectSystemError(
        shared_ptr<struct addrinfo> addresses,
        struct addrinfo** nextAddr,
        std::system_error& e,
        bool* anyRefused,
        bool* anyReset,
        bool wait) {

    handleConnectException(
            addresses,
            nextAddr,
            e.code().value(),
            anyRefused,
            anyReset,
            wait);
}

int connect(addrinfo** next_addr,
        std::shared_ptr<struct addrinfo> addresses,
        bool wait) {

    int socket;
    int errno;

    // Loop over the addresses if at least one of them gave us ECONNREFUSED
    // or ECONNRESET. This may happen if the server hasn't started listening
    // yet, or is listening but has its listen backlog exhausted.
    bool anyRefused = false;
    bool anyReset = false;

    while (true) {
        try {
            cout << "Attempting connection to: " << (*next_addr)->ai_addr << endl;
            
            //1. Initiate connection
            int ret = mock::connect(socket, **next_addr, &errno);
            if (ret != 0 && errno != EINPROGRESS) {
                throw std::system_error(errno, std::system_category());
            }

            //2. Wait for connection to complete
            int numReady = mock::poll(&errno);
            if (numReady < 0) {
                throw std::system_error(errno, std::system_category());
            } else if (numReady == 0) {
                errno = 0;
                throw std::runtime_error("Connection timeout");
            }


            //3. Check if connection succeeded or failed
            errno = 0;
            mock::getsockopt(socket, &errno);

            if (errno != 0) {
                throw std::system_error(errno, std::system_category());
            }

            break;

        } catch (std::system_error& e) {
            handleConnectSystemError(
                    addresses,
                    next_addr,
                    e,
                    &anyRefused,
                    &anyReset,
                    wait);

        } catch (std::exception& e) {

            handleConnectException(
                    addresses,
                    next_addr,
                    errno,
                    &anyRefused,
                    &anyReset,
                    wait);
        }
    }

    return socket;
}
