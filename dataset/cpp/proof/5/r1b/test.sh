echo "Compiling version without destructor implementation, that derives from a base class without a virtual destructor"

g++ SQWLoadingPresenter.cpp Base.cpp 2>&1 && echo "COMPILED AND LINKED CLEANLY" || echo "FAILED"

