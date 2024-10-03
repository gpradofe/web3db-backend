from pyspark.sql import SparkSession

class QueryEngine:
    def __init__(self):
        self.spark = SparkSession.builder             .appName("DecentralizedDB")             .config("spark.sql.warehouse.dir", "/user/hive/warehouse")             .config("hive.metastore.uris", "thrift://hive-metastore:9083")             .enableHiveSupport()             .getOrCreate()

    def execute_query(self, query):
        try:
            result = self.spark.sql(query)
            return result.toPandas()
        except Exception as e:
            return f"Error executing query: {str(e)}"

    def close(self):
        self.spark.stop()

if __name__ == "__main__":
    engine = QueryEngine()
    
    # Example usage
    result = engine.execute_query("SHOW DATABASES")
    print(result)
    
    engine.close()
