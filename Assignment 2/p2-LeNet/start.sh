#!/bin/bash
export TF_RUN_DIR="~/tf"

if [ -z $1 ]; then
    echo "Usage: ./start.sh num_of_nodes"
else
    echo "Create $TF_RUN_DIR on remote hosts if they do not exist."
    echo "Copying the script to all the remote hosts."
    for i in `seq 0 $2`; do
        ssh node$i "rm -rf $TF_RUN_DIR; mkdir -p $TF_RUN_DIR"
        scp main.py node$i:$TF_RUN_DIR
    done
    echo "Starting tensorflow servers on all hosts based on the spec in main.py"
    if [ "$2" = "1" ]; then
        nohup ssh node0 "dstat --cpu --mem --net --output report.csv" > dstat-node0.log 2>&1&
        nohup ssh node0 "cd ~/tf ; python3 main.py 1 0" > serverlog-0.out 2>&1&
    elif [ "$2" = "2" ]; then
        nohup ssh node0 "dstat --cpu --mem --net --output report.csv" > dstat-node0.log 2>&1&
        nohup ssh node1 "dstat --cpu --mem --net --output report.csv" > dstat-node1.log 2>&1&

        nohup ssh node0 "cd ~/tf ; python3 main.py 2 0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/tf ; python3 main.py 2 1" > serverlog-1.out 2>&1&
    elif [ "$2" = "3" ]; then
        nohup ssh node0 "dstat --cpu --mem --net --output report.csv" > dstat-node0.log 2>&1&
        nohup ssh node1 "dstat --cpu --mem --net --output report.csv" > dstat-node1.log 2>&1&
        nohup ssh node2 "dstat --cpu --mem --net --output report.csv" > dstat-node2.log 2>&1&

        nohup ssh node0 "cd ~/tf ; python3 main.py 3 0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/tf ; python3 main.py 3 1" > serverlog-1.out 2>&1&
        nohup ssh node2 "cd ~/tf ; python3 main.py 3 2" > serverlog-2.out 2>&1&
    fi
fi