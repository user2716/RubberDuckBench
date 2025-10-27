g++ -c test_l.cpp -o test_l.o
g++ -c test_brackets.cpp -o test_brackets.o

if ! diff -q test_l.o test_brackets.o >/dev/null 2>&1; then
    echo "Files compile to different object code"
fi

echo "Testing L\"\""
g++ test_l.o -o a.out
./a.out


echo ""
echo "Testing {}"
g++ test_brackets.o -o a.out
./a.out
