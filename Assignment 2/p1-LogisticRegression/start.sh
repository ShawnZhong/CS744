#!/bin/bash
dstat="cd ~/p1; dstat --cpu --mem --net --output report.csv &"

if [ -z $2 ]; then
    echo "Usage: start_cluster <python script> <number of worker>"
    echo "Here, <python script> contains the cluster spec that assigns an ID to all server."
else
    echo "Create ~/p1 on remote hosts if they do not exist."
    echo "Copying the script to all the remote hosts."
    for i in `seq 0 2`; do
        ssh node$i "mkdir -p ~/p1"
        scp $1 node$i:~/p1
        scp input_data.py node$i:~/p1
    done
    echo "Starting tensorflow servers on all hosts based on the spec in $1"
    echo "The server output is logged to serverlog-i.out, where i = 0, ..., 3 are the VM numbers."
    if [ "$2" = "1" ]; then
        nohup ssh node0 "$dstat" &

        nohup ssh node0 "cd ~/p1 ; python3 $1" > serverlog-0.out 2>&1&
    elif [ "$2" = "2" ]; then
        nohup ssh node0 "$dstat" &
        nohup ssh node1 "$dstat" &

        nohup ssh node0 "cd ~/p1 ; python3 $1 --deploy_mode=cluster --job_name=ps" > serverlog-ps-0.out 2>&1&
        nohup ssh node0 "cd ~/p1 ; python3 $1 --deploy_mode=cluster --task_index=0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/p1 ; python3 $1 --deploy_mode=cluster --task_index=1" > serverlog-1.out 2>&1&
    elif [ "$2" = "3" ]; then
        nohup ssh node0 "$dstat" &
        nohup ssh node1 "$dstat" &
        nohup ssh node2 "$dstat" &

        nohup ssh node0 "cd ~/p1 ; python3 $1 --deploy_mode=cluster2 --job_name=ps" > serverlog-ps-0.out 2>&1&
        nohup ssh node0 "cd ~/p1 ; python3 $1 --deploy_mode=cluster2 --task_index=0" > serverlog-0.out 2>&1&
        nohup ssh node1 "cd ~/p1 ; python3 $1 --deploy_mode=cluster2 --task_index=1" > serverlog-1.out 2>&1&
        nohup ssh node2 "cd ~/p1 ; python3 $1 --deploy_mode=cluster2 --task_index=2" > serverlog-2.out 2>&1&
    fi
fi