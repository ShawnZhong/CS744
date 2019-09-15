# CS744

## TODO
 - a1p2 set configuration


# Some useful commands
- To copy a file to hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hadoop fs -put input.csv hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/input.csv
  ```

- To list all files on hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hadoop fs -ls hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000
  ```

- To delete a file on hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hdfs dfs -rm -r -skipTrash hdfs://c240g1-031305vm-1.wisc.cloudlab.us:9000/output.csv 
  ```
