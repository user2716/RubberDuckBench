#include "2.h"
#include "Mocks.h"
#include <iostream>

using namespace std;



void test(int err_seed) {
    struct addrinfo info2;
    
    info2.ai_addr = "tcp://127.0.0.1:29500";  
    info2.ai_next = nullptr;
    info2.seed = err_seed;


    struct addrinfo info;
    
    info.ai_addr = "tcp://localhost:29500";  
    info.ai_next = &info2;
    info.seed = 3; 

    addrinfo* head_addr = &info;

    std::shared_ptr<struct addrinfo> addresses(&info, [](addrinfo*){});

    try {
        connect(&head_addr, addresses, true);
    } catch(std::system_error e) {

    }

}

int main() {

    cout << "Testing an example with a connection list of 2 addresses for which neither fail with refusal or reset." << endl;
    cout << "-------------------------------------------------------------------------------------------------------" << endl;
    test(10); //try connection with a list of 2 addresses (non refusal or reset)
    cout << endl;
    cout << endl;
    


    cout << "Testing an example with a connection list of 2 addresses for which one fails with refusal." << endl;
    cout << "-------------------------------------------------------------------------------------------------------" << endl;
    test(9); //try connection with a list of 2 addresses (one refusal)
    
    /*
     *  1. error code can be something other than REFUSED or RESET
     *  2. reset and refusal affects connection retry
     *  3. If any error type is thrown the program attempts to connect to the next address 
     *      -> NOT JUST REFUSAL OR RESET
     *  4. If all addresses have been tried without a successful connection, and at least one resulted in a REFUSAL or RESET, the program keeps looping
     *  5. If all addresses have been tried and none of them resulted in REFUSAL or RESET, an error is thrown and no reconnection is attepmted
     */

}
