#ifndef SQW_H
#define SQW_H

#include "Base.h"
#include <string>


class SQWLoadingPresenter : Base {

    public:
        SQWLoadingPresenter(const std::string);

    private:
        const std::string m_filename;
        std::string m_wsTypeName; 
};

#endif
