#Shows that a virtual destructor in the base class does not necessitate a destructor in the child

echo "Compiling version without destructor implementation, that derives from a base class with a virtual destructor"

g++ SQWLoadingPresenter.cpp Base.cpp 2>&1 && echo "COMPILED AND LINKED CLEANLY" || echo "FAILED"

