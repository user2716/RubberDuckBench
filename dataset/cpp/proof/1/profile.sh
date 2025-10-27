#Install fmt library 
#sudo apt install libfmt-dev

g++ test_format.cpp -lfmt
echo "test with fmt"
./a.out chowajksldf aa  #print timing info
#valgrind --tool=massif --detailed-freq=1 --time-unit=B --massif-out-file=fmt.out ./a.out chowajksldf aa

echo "test with concat"
g++ test_concat.cpp -lfmt
./a.out chowajksldf aa  #print timing info
#valgrind --tool=massif --detailed-freq=1 --time-unit=B --massif-out-file=concat.out ./a.out chowajksldf aa

massif-visualizer concat.out &
massif-visualizer fmt.out &
