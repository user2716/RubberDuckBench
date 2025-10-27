#ifndef SQW_H
#define SQW_H

#include <string>


class SQWLoadingPresenter {

    public:
        SQWLoadingPresenter(const std::string);
        virtual ~SQWLoadingPresenter();  

    private:
        const std::string m_filename;
        std::string m_wsTypeName; 
};

#endif
