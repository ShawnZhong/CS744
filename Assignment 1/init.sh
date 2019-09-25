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
<value>hdfs://c220g1-030823vm-1.wisc.cloudlab.us:9000</value>
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


echo "c220g1-030823vm-2.wisc.cloudlab.us
c220g1-030823vm-3.wisc.cloudlab.us" > hadoop-3.1.2/etc/hadoop/workers

echo \
'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> hadoop-3.1.2/etc/hadoop/hadoop-env.sh


# spark
wget http://mirror.metrocast.net/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar zvxf spark-2.4.4-bin-hadoop2.7.tgz

echo "c220g1-030823vm-2.wisc.cloudlab.us
c220g1-030823vm-3.wisc.cloudlab.us" > spark-2.4.4-bin-hadoop2.7/conf/slaves

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuRNY6/5CsdCnQ6ZTrzu7EHRcvqhU9ideUDRCrnr92NLL7yDQ01tL9OHK5m6UBso90Px6++5F6y/h7HbsA+EcZK6M7sen4g3VvWgO49sumZWsbRlqqviKROxEjdr9rD4NV17GMFlNDI128v9XQv4wbQqQ7v+vVWNnodbTDcZaF1L72hF8Y+/dvsvajMEzVBhdUVs/1IN/5i1ABMsZmpRwu6BI1xm2492bnFMrpyPI1xD9Nb5A/9LtjFenyPYIUqKDhNyKlejb3dKwON3PyPF/aQZ3VPQ/cWBUCQ0hJYzNJbLhfFY1wvVtKpA5v99Zcvh/raIVx1niBJNbOPuv8c8px szhong@node0.szhong-qv58271.uwmadison744-f19-pg0.wisc.cloudlab.us" >> ~/.ssh/authorized_keys