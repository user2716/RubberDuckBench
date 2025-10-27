#include <iostream>
#include <string>
#include <cstdlib>
#include <vector>
#include <thread>
#include <chrono>
#include <future>
#include "errno.h"
#include "Mocks.h"

using namespace std;


namespace mock {

    int connect(int socket, const addrinfo& addr, int* error_code) {
        std::this_thread::sleep_for(std::chrono::seconds(1));

        int error_codes[] = {
            0,
            EACCES,
            EPERM,
            EADDRINUSE,
            EADDRNOTAVAIL,
            EAFNOSUPPORT,
            EAGAIN,
            EALREADY,
            EBADF,
            ECONNREFUSED,
            EFAULT,
            EINPROGRESS,
            EINTR,
            EISCONN,
            ENETUNREACH,
            ENOTSOCK,
            EPROTOTYPE,
            ETIMEDOUT
        };

        //#int num_errors = sizeof(error_codes) / sizeof(error_codes[0]);

        int err = error_codes[addr.seed];

        *error_code = err;

        if (error_code == 0) {
            return 0;
        } else {
            return -1;
        }
    }

    int poll(int* error_code) {
        int error_codes[] = {
            0,           // No error (success)
            EFAULT,    
            EINTR,      
            EINVAL, 
            ENOMEM        
        };

        int num_errors = sizeof(error_codes) / sizeof(error_codes[0]);
        int random_error = error_codes[rand() % num_errors];

        *error_code = random_error;

        if (error_code == 0) {
            return 0;
        } else {
            return -1;
        }
    }

    void getsockopt(int socket, int* error_code) {
        int error_codes[] = {
            0,           // No error (success)
            EBADF,       
            EFAULT,      
            EINVAL,      
            ENOPROTOOPT, 
            ENOTSOCK,    
            EACCES,      
            ENOBUFS,     
            ENOSR        
        };

        int num_errors = sizeof(error_codes) / sizeof(error_codes[0]);
        int random_error = error_codes[rand() % num_errors];

        *error_code = random_error;

    }

}
