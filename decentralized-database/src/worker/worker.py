import os
import time
from pyspark.sql import SparkSession

def create_spark_session():
    return SparkSession.builder \
        .appName("DecentralizedDBWorker") \
        .config("spark.master", "spark://spark-master:7077") \
        .getOrCreate()

def main():
    print("Worker node starting...")
    
    # Read node configuration
    with open('/app/node.conf', 'r') as f:
        config = dict(line.strip().split('=') for line in f if '=' in line)
    
    # Set up Spark session
    spark = create_spark_session()
    
    while True:
        # TODO: Implement worker logic
        # - Listen for tasks from the master node
        # - Execute tasks using Spark
        # - Report results back to the master node
        print("Worker node running...")
        time.sleep(60)

if __name__ == "__main__":
    main()