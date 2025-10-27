#include "SQWLoadingPresenter.h"

#include <iostream>

SQWLoadingPresenter::SQWLoadingPresenter(std::unique_ptr<MDLoadingView> view, const std::string filename)
    : Base(std::move(view)), m_wsTypeName(""), m_filename(filename) {}


SQWLoadingPresenter::~SQWLoadingPresenter() {} //Line in question

int main() {

}
