#!/bin/bash
export TF_RUN_DIR="~/tf"

function terminate_cluster() {
    echo "Terminating the servers"
#    CMD="ps aux | grep -v 'grep' | grep 'python code_template' | awk -F' ' '{print $2}' | xargs kill -9"
    CMD="ps aux | grep -v 'grep' | grep -v 'bash' | grep -v 'ssh' | grep 'python code_template' | awk -F' ' '{print \$2}' | xargs kill -9"
    for i in `seq 0 2`; do
        ssh node$i "$CMD"
    done
}


function install_tensorflow() {
    for i in `seq 0 2`; do
        nohup ssh node$i "sudo apt update; sudo apt install --assume-yes python3-pip python3-dev; sudo pip install tensorflow"
    done
}


function start_cluster() {
    if [ -z $2 ]; then
        echo "Usage: start_cluster <python script> <cluster mode>"
        echo "Here, <python script> contains the cluster spec that assigns an ID to all server."
    else
        echo "Create $TF_RUN_DIR on remote hosts if they do not exist."
        echo "Copying the script to all the remote hosts."
        for i in `seq 0 2`; do
            ssh node$i "mkdir -p $TF_RUN_DIR"
            scp $1 node$i:$TF_RUN_DIR
        done
        echo "Starting tensorflow servers on all hosts based on the spec in $1"
        echo "The server output is logged to serverlog-i.out, where i = 0, ..., 3 are the VM numbers."
        if [ "$2" = "single" ]; then
            nohup ssh node0 "cd ~/tf ; python3 $1 --deploy_mode=single" > serverlog-0.out 2>&1&
        elif [ "$2" = "cluster" ]; then
            nohup ssh node0 "cd ~/tf ; python3 $1 --deploy_mode=cluster  --job_name=ps" > serverlog-ps-0.out 2>&1&
            nohup ssh node0 "cd ~/tf ; python3 $1 --deploy_mode=cluster  --task_index=0" > serverlog-0.out 2>&1&
            nohup ssh node1 "cd ~/tf ; python3 $1 --deploy_mode=cluster  --task_index=1" > serverlog-1.out 2>&1&
        else
            nohup ssh node0 "cd ~/tf ; python3 $1 --deploy_mode=cluster2  --job_name=ps" > serverlog-ps-0.out 2>&1&
            nohup ssh node0 "cd ~/tf ; python3 $1 --deploy_mode=cluster2  --task_index=0" > serverlog-0.out 2>&1&
            nohup ssh node1 "cd ~/tf ; python3 $1 --deploy_mode=cluster2  --task_index=1" > serverlog-1.out 2>&1&
            nohup ssh node2 "cd ~/tf ; python3 $1 --deploy_mode=cluster2  --task_index=2" > serverlog-2.out 2>&1&
        fi
    fi
}
