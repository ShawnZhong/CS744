#!/bin/bash

rm -rf summary
rm -rf *.log
rm -rf *.out
rm -rf report.csv

CMD="rm -rf ~/p2;"
for i in `seq 0 2`; do
    echo "Cleaning the server $i"
    ssh node$i "$CMD"
done