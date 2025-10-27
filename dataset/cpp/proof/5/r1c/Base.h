#ifndef BASE_H
#define BASE_H

#include <string>

class Base {
    public:
        Base();

    protected:
        std::string name_;

    private:
        virtual ~Base();    

};

#endif
