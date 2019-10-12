# Usage
To run this application, use the following

./run.sh <main_async.py or main_sync.py> <number of workers: 1, 2, or 3>

Example: 

- Run async SGD on a single machine: `./run.sh main_async.py 1`

- Run sync SGD on 3 machines: `./run.sh main_sync.py 3`

# Assumptions 
The machine should have Python 3.5.2 and Tensorflow 1.14.0 installed