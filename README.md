# CS744

### Verify Hadoop and Spark with host and port

- To check Hadoop:
http://clnodevm053-1.clemson.cloudlab.us:9870/dfshealth.html

- To check Spark:
http://clnodevm053-1.clemson.cloudlab.us:8080/

### TODO
 - a1p2 set configuration


### Some useful commands
- To copy a file to hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hadoop fs -put input.csv hdfs://clnodevm053-1.clemson.cloudlab.us:9000/input.csv
  ```

- To list all files on hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hadoop fs -ls hdfs://clnodevm053-1.clemson.cloudlab.us:9000
  ```

- To delete a file on hdfs

  ```sh
  ~/hadoop-3.1.2/bin/hdfs dfs -rm -r -skipTrash hdfs://clnodevm053-1.clemson.cloudlab.us:9000/output.csv 
  ```
