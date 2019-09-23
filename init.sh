#!/bin/sh

# Install deps
sudo apt-get update
sudo apt-get install openjdk-8-jdk python-pip -y
pip install pyspark

# Part 0: 
sudo mkfs.ext4 /dev/xvda4
# This formats the partition to be of type ext4
sudo mkdir -p /mnt/data 
# Create a directory where the filesystem will be mounted
sudo mount /dev/xvda4 /mnt/data 
# Mount the partition at the particular directory

# Part 1:
# hadoop
wget http://apache.mirrors.hoobly.com/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz
tar zvxf hadoop-3.1.2.tar.gz

echo \
'<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://clnodevm053-1.clemson.cloudlab.us:9000</value>
</property>
</configuration>' > hadoop-3.1.2/etc/hadoop/core-site.xml

echo \ 
'<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
<property>
<name>dfs.namenode.name.dir</name>
<value>hadoop-3.1.2/data/namenode/</value>
</property>
<property>
<name>dfs.datanode.data.dir</name>
<value>hadoop-3.1.2/data/datanode/</value>
</property>
</configuration>' > hadoop-3.1.2/etc/hadoop/hdfs-site.xml


echo "clnodevm053-2.clemson.cloudlab.us
clnodevm053-3.clemson.cloudlab.us" > hadoop-3.1.2/etc/hadoop/workers

echo \
'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> hadoop-3.1.2/etc/hadoop/hadoop-env.sh


# spark
# wget http://mirror.metrocast.net/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
wget http://apache-mirror.8birdsvideo.com/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar zvxf spark-2.4.4-bin-hadoop2.7.tgz

echo "clnodevm053-2.clemson.cloudlab.us
clnodevm053-3.clemson.cloudlab.us" > spark-2.4.4-bin-hadoop2.7/conf/slaves

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAaKwN8c6Xgoxc1iD42VbUxMq8QIvX9vCElv4evu77ie1kvO4c4dx10zmy8jsk3ME+vpaxwuDWTtKrAvm53PsL7XY5a4Lnfc59k8PCQxvPJOhAaVcGh83lhnMKjVDPqExP3sYo6aQU2OAT0/eVb0CDXlvdbpeGIw8ItHNgituft2Yql5tsQXxciL9GOKbr5GMUnyyscrSt+rdRqa1CMsA8GwSNzhfLNMTqZmBOjKdTkaPSKGzviPqRJewM2TW3qJ3FZpBSwN5fsDWCWJ96I/jVJhheF4BqEyZ8y+LZIeUi5fSZqhrzRyVPWg9NCyJYBd9DVy6mAoSwlFIb0YXJ9Kuv szhong@node0.ainuratestexp.uwmadison744-f19-pg0.wisc.cloudlab.us" >> ~/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLZTYPW9ZzVJ7LnXKHINUIX9tUjoE5ftJQRgsPjfen3OpyOWQN83Hl+4H0Rk3eWT/hBox37hRTmRo6AgKaA0vagIZzDNplGUZscLaXzeIVflw0oCFFZ1nhLP1hvl/z8gXOyZsX7UZGyn16qldWM+J98SmaahEYM+sFv/+p1ZAcvKHA8l6XyRqjAZxQvHDxzkM/CsgANwVAF4wGMX92Ix5dLIwErbxSISQPhn25xHm0B81KLeowuLDkaZiL5vk4+tNHKLO4HQmHdBRfWnmzXOL8oaqTvGbPBg02AE4ys6uGZKZJFYfmr+hz2qqK4lUaIs4YWwVXf4ZGww3cNCig0H0Z szhong@node0.squ27-hw1.uwmadison744-f19-pg0.clemson.cloudlab.us" >> ~/.ssh/authorized_keys