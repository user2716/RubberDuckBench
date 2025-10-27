echo "Compiling a version of Base with a private destructor. Note that the actual implementation's Base class is public."

g++ SQWLoadingPresenter.cpp Base.cpp 2>&1 && echo "COMPILED AND LINKED CLEANLY" || echo "DID NOT COMPILE CLEANLY"

