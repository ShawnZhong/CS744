#!/bin/bash

# cluster_utils.sh has helper function to start process on all VMs
# it contains definition for start_cluster and terminate_cluster
source cluster_utils.sh
start_cluster code_template.py single

# defined in cluster_utils.sh to terminate the cluster
# terminate_cluster
