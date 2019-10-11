#!/bin/bash
CMD="killall dstat; killall python3;"
for i in `seq 0 2`; do
    echo "Terminating the server $i"
    ssh node$i "$CMD"
done