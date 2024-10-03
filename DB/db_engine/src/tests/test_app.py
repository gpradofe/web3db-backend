import unittest
from flask import Flask
from flask_restx import Api
from src import api, p2p_manager, query_engine

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_get_peers(self):
        response = self.app.get('/peers/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('peers', data)

    def test_connect_to_peer(self):
        peer_addr = "127.0.0.1:7175"
        response = self.app.post('/peers/', data=json.dumps({'peer_addr': peer_addr}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_execute_query(self):
        # Create a test table
        create_query = "CREATE TABLE test_table (id INT, name STRING)"
        response = self.app.post('/query/', data=json.dumps({'query': create_query}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Insert test data
        insert_query = "INSERT INTO test_table VALUES (1, 'test')"
        response = self.app.post('/query/', data=json.dumps({'query': insert_query}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test selecting data
        select_query = "SELECT * FROM test_table"
        response = self.app.post('/query/', data=json.dumps({'query': select_query}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)
        self.assertEqual(len(data['result']), 1)
        self.assertEqual(data['result'][0]['id'], 1)
        self.assertEqual(data['result'][0]['name'], 'test')

if __name__ == '__main__':
    unittest.main()