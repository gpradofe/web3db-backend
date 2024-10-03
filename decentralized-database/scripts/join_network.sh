#!/bin/bash

# Start IPFS daemon (for master nodes)
if [ -f /data/ipfs/config ]; then
    ipfs daemon &
fi

# Join Hadoop cluster
hdfs dfsadmin -refreshNodes

# Join Spark cluster
$SPARK_HOME/sbin/start-slave.sh spark://spark-master:7077

echo "Node has joined the network."