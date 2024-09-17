import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'
    
    # Database
    DB_ENGINE_PORT = int(os.getenv('DB_ENGINE_PORT', 3001))
    
    # P2P
    P2P_PORT = int(os.getenv('P2P_PORT', 8000))
    KNOWN_PEERS = os.getenv('KNOWN_PEERS', '').split(',')
    
    # IPFS
    IPFS_API_URL = os.getenv('IPFS_API_URL', 'http://ipfs:5001')
    
    # Spark
    SPARK_MASTER = os.getenv('SPARK_MASTER', 'spark://spark-master:7077')
    
    # Hive
    HIVE_METASTORE_URI = os.getenv('HIVE_METASTORE_URI', 'thrift://hive-metastore:9083')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_config(cls):
        return {key: value for key, value in cls.__dict__.items() if not key.startswith('__') and not callable(value)}