import unittest
import requests
import time
import json
from src.app import app

class TestIntegration(unittest.TestCase):
    BASE_URL = "http://db_engine:3001"

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        # Wait for the service to start
        time.sleep(5)

    def test_peer_connection(self):
        # Test connecting to a peer
        response = self.app.post('/peers/', json={"peer_addr": "127.0.0.1:7175"})
        self.assertEqual(response.status_code, 200)

        # Test getting connected peers
        response = self.app.get('/peers/')
        self.assertEqual(response.status_code, 200)
        peers = response.json["peers"]
        self.assertIsInstance(peers, list)

    def test_query_execution(self):
        # Test creating a table
        create_query = "CREATE TABLE test_table (id INT, name STRING)"
        response = self.app.post('/query/', json={"query": create_query})
        self.assertEqual(response.status_code, 200)

        # Test inserting data
        insert_query = "INSERT INTO test_table VALUES (1, 'test')"
        response = self.app.post('/query/', json={"query": insert_query})
        self.assertEqual(response.status_code, 200)

        # Test selecting data
        select_query = "SELECT * FROM test_table"
        response = self.app.post('/query/', json={"query": select_query})
        self.assertEqual(response.status_code, 200)
        result = response.json["result"]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["name"], "test")

    def test_state_restoration(self):
        # Assume we have a method to get the current state hash
        state_hash = self.get_current_state_hash()

        # Test querying with state restoration
        query = "SELECT * FROM test_table"
        response = self.app.post('/query/', json={"query": query, "hash": state_hash})
        self.assertEqual(response.status_code, 200)
        result = response.json["result"]
        self.assertGreater(len(result), 0)

    def get_current_state_hash(self):
        # This method should be implemented to get the current state hash
        # For now, we'll return a dummy hash
        return "QmDummyHash"

if __name__ == "__main__":
    unittest.main()