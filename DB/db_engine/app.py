from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import requests
import subprocess
from pyspark.sql import SparkSession
import os

app = Flask(__name__)
api = Api(app, version='1.0', title='IPFS Hive Query API', description='A simple API using Flask-Restx and IPFS')


IPFS_API_URL = os.environ.get('IPFS_API_URL', "http://ipfs:5001")
SPARK_MASTER = os.environ.get('SPARK_MASTER', 'spark://spark-master:7077')

class DBManager:

    @staticmethod
    def dump_database():
        dump_filename = "/dumps/full_dump.sql"
        subprocess.call(["pg_dumpall", ">", dump_filename])

        with open(dump_filename, 'r') as f:
            return f.read()

    @staticmethod
    def recreate_from_dump(sql_dump):
        dump_filename = "/dumps/temp_dump.sql"
        with open(dump_filename, 'w') as f:
            f.write(sql_dump)
        subprocess.call(["psql", "<", dump_filename])
    
    @staticmethod
    def create_table(query):
        subprocess.call(["psql", "-c", query])
        return "Table created successfully"



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
    def execute_query(query):
        spark = SparkSession.builder \
            .appName("IPFS Hive Query Engine") \
            .enableHiveSupport() \
            .master(SPARK_MASTER) \
            .getOrCreate()

        result = spark.sql(query)
        return result.collect()


query_ns = api.namespace('query', description='Query operations')

@query_ns.route('/')
class QueryResource(Resource):

    @api.expect(api.model('Query', {
        'query': api.String(required=True, description='SQL Query'),
        'metamask_key': api.String(required=True, description='Metamask Key'),
        'hash': api.String(required=True, description='IPFS Hash'),
    }))
    def post(self):
        '''Execute a query and return the results'''
        query = request.json.get("query")
        metamask_key = request.json.get("metamask_key")
        data_hash = request.json.get("hash")

        if 'CREATE TABLE' in query.upper():
            message = DBManager.create_table(query)
            new_sql_dump = DBManager.dump_database()
            new_ipfs_hash = IPFSManager.upload_to_ipfs(new_sql_dump)
            return {"message": message, "new_hash": new_ipfs_hash}

        sql_dump = IPFSManager.fetch_sql_dump_from_ipfs(data_hash)
        DBManager.recreate_from_dump(sql_dump)
        result = QueryEngine.execute_query(query)

        if 'UPDATE' in query.upper() or 'INSERT' in query.upper() or 'DELETE' in query.upper():
            new_sql_dump = DBManager.dump_database()
            new_ipfs_hash = IPFSManager.upload_to_ipfs(new_sql_dump)
            return {"message": "Query executed and database updated", "data": result, "new_hash": new_ipfs_hash}

        return {"message": "Query executed successfully", "data": result}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
