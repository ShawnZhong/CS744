#!/bin/bash
dstat="cd ~/p2; dstat --cpu --mem --net --output report.csv &"

if [ -z $1 ]; then
    echo "Usage: ./start.sh num_of_nodes"
else
    echo "Create p2 on remote hosts if they do not exist."
    echo "Copying the script to all the remote hosts."
    for i in `seq 0 $1`; do
        ssh node$i "mkdir -p ~/p2"
        scp main.py node$i:~/p2
    done
    echo "Starting tensorflow servers on all hosts based on the spec in main.py"
    if [ "$1" = "1" ]; then
        nohup ssh node0 "$dstat" &
        nohup ssh node0 "cd ~/p2 ; python3 main.py 1 0" > serverlog-0.out 2>&1&
    elif [ "$1" = "2" ]; then
        nohup ssh node0 "$dstat" &
        nohup ssh node1 "$dstat" &

        nohup ssh node0 "cd ~/p2 ; python3 main.py 2 0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/p2 ; python3 main.py 2 1" > serverlog-1.out 2>&1&
    elif [ "$1" = "3" ]; then
        nohup ssh node0 "$dstat" &
        nohup ssh node1 "$dstat" &
        nohup ssh node2 "$dstat" &

        nohup ssh node0 "cd ~/p2 ; python3 main.py 3 0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/p2 ; python3 main.py 3 1" > serverlog-1.out 2>&1&
        nohup ssh node2 "cd ~/p2 ; python3 main.py 3 2" > serverlog-2.out 2>&1&
    fi
fi