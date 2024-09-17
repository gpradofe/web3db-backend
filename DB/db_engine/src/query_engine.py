from pyspark.sql import SparkSession
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class QueryEngine:
    def __init__(self):
        self.config = Config.get_config()
        self.spark = self._create_spark_session()

    def _create_spark_session(self):
        return SparkSession.builder \
            .appName("Web3DB Query Engine") \
            .master(self.config['SPARK_MASTER']) \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .config("hive.metastore.uris", self.config['HIVE_METASTORE_URI']) \
            .enableHiveSupport() \
            .getOrCreate()

    def execute_query(self, query, sql_dump=None):
        try:
            if sql_dump:
                self._restore_state(sql_dump)
            
            result = self.spark.sql(query).collect()
            return [row.asDict() for row in result]
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise

    def _restore_state(self, sql_dump):
        try:
            queries = json.loads(sql_dump)
            for q in queries:
                self.spark.sql(q)
        except Exception as e:
            logger.error(f"Failed to restore state: {str(e)}")
            raise

query_engine = QueryEngine()