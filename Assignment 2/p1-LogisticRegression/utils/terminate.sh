#!/bin/bash

echo "Terminating the servers"
CMD="ps aux | grep -v 'grep' | grep -v 'bash' | grep -v 'ssh' | grep 'python code_template' | awk -F' ' '{print \$2}' | xargs kill -9"
for i in `seq 0 2`; do
    ssh node$i "$CMD"
done