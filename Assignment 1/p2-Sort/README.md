# Overview
This application takes in a csv file, sorts it by the third and last column, and save the sorted file in to a specified location. 

# Usage
To run this application, use the following

```sh
python sort.py [path to input file] [path to output file]
```

Example: 
```sh
python sort.py hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/input.csv hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/output.csv
```

# Assumptions 
The machine should have Python 2.7 (with pyspark), Hadoop, and Spark installed. 
