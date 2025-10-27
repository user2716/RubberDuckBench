#Shows that destructor implementation is needed when its declared as virtual in the header

echo "Compiling version without destructor implementation"

g++ SQWLoadingPresenter_mod.cpp 2>&1 | grep -qiE "(undefined reference|ld returned|collect2: error)" && echo "LINKER ERROR DETECTED"

echo ""

echo "Compiling version with destructor implementation"
g++ SQWLoadingPresenter.cpp 2>&1 && echo "COMPILED AND LINKED CLEANLY" || echo "FAILED"
