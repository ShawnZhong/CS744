# Overview
This application takes in a csv file, sorts it by the third and last column, and save the sorted file in to a specified location. 

# Usage
To run this application, use the following

```sh
python a1p2.py [path to input file] [path to output file]
```

Example: 
```sh
python a1p2.py hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/input.csv hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/output.csv
```

# Assumptions 
The machine should have Python 2.7 (with pyspark), Hadoop, and Spark installed. 


# Some useful commands
- To copy a file to hdfs

  ~/hadoop-3.1.2/bin/hadoop fs -put input.csv hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/input.csv

- To list all files on hdfs

  ~/hadoop-3.1.2/bin/hadoop fs -ls hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000

- To delete a file on hdfs

  ~/hadoop-3.1.2/bin/hdfs dfs -rm -r -skipTrash hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/output.csv 
