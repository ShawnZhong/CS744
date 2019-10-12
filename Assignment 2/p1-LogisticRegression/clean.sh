#!/bin/bash

rm -f *.out 
rm -f report.csv
rm -rf MNIST_data

CMD="rm -rf ~/p1;"
for i in `seq 0 2`; do
    echo "Cleaning the server $i"
    ssh node$i "$CMD"
done