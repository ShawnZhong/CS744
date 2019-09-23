# format the namenode and start the namymenode daemon
hadoop-3.1.2/bin/hdfs namenode -format
hadoop-3.1.2/sbin/start-dfs.sh

# start spark standalone cluster
spark-2.4.4-bin-hadoop2.7/sbin/start-all.sh

# stop cluster
spark-2.4.4-bin-hadoop2.7/sbin/stop-all.sh