#!/bin/bash

echo "Starting all tests..."

echo "Testing IPFS..."
docker-compose exec -T ipfs ipfs id
docker-compose exec -T ipfs ipfs add -q /etc/hosts

echo "Testing Hadoop..."
docker-compose exec -T hadoop-namenode hdfs dfs -mkdir /test
docker-compose exec -T hadoop-namenode hdfs dfs -ls /

echo "Testing YARN..."
docker-compose exec -T resourcemanager yarn node -list

echo "Testing Spark..."
cat << PYTHON > test.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()
df = spark.createDataFrame([(1, "test")], ["id", "value"])
df.show()
spark.stop()
PYTHON
docker-compose exec -T spark-master bash -c "cat > /opt/spark/test.py << EOF
$(cat test.py)
EOF
"
docker-compose exec -T spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/test.py

echo "Testing Hive Metastore..."
docker-compose exec -T hive-metastore /opt/hive/bin/schematool -dbType postgres -info

echo "Testing Hive Server..."
docker-compose exec -T hive-server beeline -u jdbc:hive2://localhost:10000 -e "SHOW DATABASES;"

echo "Running Integration Test..."
cat << PYTHON > test_integration.py
from pyspark.sql import SparkSession
import traceback

try:
    spark = SparkSession.builder \
        .appName("IntegrationTest") \
        .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
        .enableHiveSupport() \
        .getOrCreate()

    # Create a test table in Hive
    spark.sql("CREATE TABLE IF NOT EXISTS test_table (id INT, value STRING)")
    spark.sql("INSERT INTO test_table VALUES (1, 'test')")

    # Read the table and show results
    result = spark.sql("SELECT * FROM test_table")
    result.show()

    spark.stop()
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print(traceback.format_exc())
PYTHON
docker-compose exec -T spark-master bash -c "cat > /opt/spark/test_integration.py << EOF
$(cat test_integration.py)
EOF
"
docker-compose exec -T spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 --jars /opt/spark/jars/postgresql-42.6.0.jar /opt/spark/test_integration.py

echo "All tests completed."