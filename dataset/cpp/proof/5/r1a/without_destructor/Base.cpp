#include "Base.h"
#include <iostream>


Base::Base(std::unique_ptr<MDLoadingView> view): name_("Parent"), m_view(std::move(view)) {}

Base::~Base() {}

