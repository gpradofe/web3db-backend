from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import requests
from pyspark.sql import SparkSession
import os
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='IPFS Hive Query API', description='A simple API using Flask-RestX and IPFS')

IPFS_API_URL = os.environ.get('IPFS_API_URL', "http://ipfs:5001")
SPARK_MASTER = os.environ.get('SPARK_MASTER', 'spark://spark-master:7077')

class IPFSManager:
    @staticmethod
    def upload_to_ipfs(data):
        files = {'file': ('dump.sql', data)}
        response = requests.post(f"{IPFS_API_URL}/api/v0/add", files=files)
        if response.status_code == 200:
            ipfs_hash = response.json().get("Hash")
            return ipfs_hash
        else:
            raise ConnectionError(f"Failed to upload data to IPFS. Status code: {response.status_code}")

    @staticmethod
    def fetch_sql_dump_from_ipfs(data_hash):
        response = requests.get(f"{IPFS_API_URL}/api/v0/cat?arg={data_hash}")
        if response.status_code == 200:
            return response.text
        else:
            raise ConnectionError(f"Failed to fetch data from IPFS. Status code: {response.status_code}")

class QueryEngine:
    @staticmethod
    def execute_query(query, sql_dump=None):
        spark = SparkSession.builder \
            .appName("IPFS Hive Query Engine") \
            .master(SPARK_MASTER) \
            .enableHiveSupport() \
            .getOrCreate()

        # Re-create database state from dump
        if sql_dump:
            queries = json.loads(sql_dump)
            for q in queries:
                spark.sql(q)

        # Execute the current query
        result = spark.sql(query).collect()
        return result

query_ns = api.namespace('query', description='Query operations')

query_model = api.model('Query', {
    'query': fields.String(required=True, description='SQL Query'),
    'hash': fields.String(description='IPFS Hash of the existing database state'),
})

@query_ns.route('/')
class QueryResource(Resource):
    @api.expect(query_model)
    def post(self):
        '''Execute a query and return the results'''
        query = request.json.get("query")
        data_hash = request.json.get("hash")

        try:
            modifying_queries = []

            # Skip IPFS fetch for dummy hash or CREATE TABLE queries
            if data_hash != "dummy_ipfs_hash" and 'CREATE TABLE' not in query.upper():
                try:
                    sql_dump = IPFSManager.fetch_sql_dump_from_ipfs(data_hash)
                    modifying_queries = json.loads(sql_dump)
                except requests.exceptions.RequestException as e:
                    return {"error": f"Failed to fetch data from IPFS: {str(e)}"}, 500

            # Execute the query
            result = QueryEngine.execute_query(query, sql_dump if data_hash != "dummy_ipfs_hash" and 'SELECT' not in query.upper() else None)

            if 'SELECT' not in query.upper():
                # Update the dump for modifying queries
                modifying_queries.append(query)
                new_dump = json.dumps(modifying_queries)
                new_ipfs_hash = IPFSManager.upload_to_ipfs(new_dump)
                return {"message": "Query executed successfully", "data": result, "new_hash": new_ipfs_hash}
            else:
                # For SELECT queries, just return the result
                return {"data": result}

        except Exception as e:
            return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
