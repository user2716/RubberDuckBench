#ifndef BASE_H
#define BASE_H

#include <string>
#include <memory>

struct MDLoadingView {
    std::string view;
};

class Base {
    public:
        Base(std::unique_ptr<MDLoadingView> view);
        virtual ~Base();    

    protected:
        std::string name_;
        std::unique_ptr<MDLoadingView> m_view;

};

#endif
