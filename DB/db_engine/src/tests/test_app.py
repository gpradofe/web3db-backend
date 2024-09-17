import unittest
from flask import json
from src.app import app

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
        peer_addr = "/ip4/127.0.0.1/tcp/8000/p2p/QmYyQSo1c1Ym7orWxLYvCrM2EmxFTANf8wXmmE7DWjhx5N"
        response = self.app.post('/peers/', data=json.dumps({'peer_addr': peer_addr}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_execute_query(self):
        query = "SELECT * FROM test_table LIMIT 10"
        response = self.app.post('/query/', data=json.dumps({'query': query}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

if __name__ == '__main__':
    unittest.main()