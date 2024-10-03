from pyspark.sql import SparkSession
import traceback

try:
    spark = SparkSession.builder         .appName("IntegrationTest")         .config("hive.metastore.uris", "thrift://hive-metastore:9083")         .enableHiveSupport()         .getOrCreate()

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
