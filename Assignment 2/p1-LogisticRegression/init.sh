#!/bin/bash

for i in `seq 0 2`; do
    nohup ssh node$i "sudo apt update; sudo apt install --assume-yes python3-pip python3-dev; sudo pip3 install tensorflow tensorflow-datasets absl-py"
done