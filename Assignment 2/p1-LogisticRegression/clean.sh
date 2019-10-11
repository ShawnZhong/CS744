#!/bin/bash

rm -f *.out

CMD="rm -rf ~/tf;"
for i in `seq 0 2`; do
    echo "Cleaning the server $i"
    ssh node$i "$CMD"
done