import unittest
from src.query_engine import QueryEngine

class TestQueryEngine(unittest.TestCase):
    def setUp(self):
        self.query_engine = QueryEngine()

    def test_execute_query(self):
        # This test assumes you have a test database set up
        query = "SELECT * FROM test_table LIMIT 10"
        result = self.query_engine.execute_query(query)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 10)

    def test_restore_state(self):
        sql_dump = '[{"CREATE TABLE test_table (id INT, name STRING)"},{"INSERT INTO test_table VALUES (1, \'test\')}]'
        self.query_engine._restore_state(sql_dump)
        result = self.query_engine.execute_query("SELECT * FROM test_table")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], 'test')

if __name__ == '__main__':
    unittest.main()