#echo "Ensuring that the destructor is equivalent to the compiler created one"

extract_instructions() {
    grep -E '^\s+(mov|call|push|pop|add|sub|lea|jmp|je|jne|ret|nop|endbr64)' "$1" | \
    sed 's/\.L[0-9]\+/.LABEL/g' | \
    sort
}

cd with_destructor
g++ -S -masm=intel -O0 SQWLoadingPresenter.cpp Base.cpp

cd ../without_destructor
g++ -S -masm=intel -O0 SQWLoadingPresenter.cpp Base.cpp

cd ../

echo "Comparing assembly..."
diff -u <(extract_instructions with_destructor/SQWLoadingPresenter.s) \
        <(extract_instructions without_destructor/SQWLoadingPresenter.s)

if [ $? -eq 0 ]; then
    echo "Identical CPU instructions - No functional difference when destructor is removed"
else
    echo "Different CPU instructions - Difference when destructor is removed"
fi
