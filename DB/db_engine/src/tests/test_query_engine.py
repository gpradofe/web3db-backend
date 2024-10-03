import unittest
from src.query_engine import QueryEngine

class TestQueryEngine(unittest.TestCase):
    def setUp(self):
        self.query_engine = QueryEngine()

    def test_execute_query(self):
        # Create a test table
        create_query = "CREATE TABLE test_table (id INT, name STRING)"
        self.query_engine.execute_query(create_query)

        # Insert test data
        insert_query = "INSERT INTO test_table VALUES (1, 'test')"
        self.query_engine.execute_query(insert_query)

        # Test selecting data
        select_query = "SELECT * FROM test_table"
        result = self.query_engine.execute_query(select_query)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], 'test')

    def test_restore_state(self):
        sql_dump = '[{"CREATE TABLE test_table (id INT, name STRING)"},{"INSERT INTO test_table VALUES (1, \'test\')}]'
        self.query_engine._restore_state(sql_dump)
        result = self.query_engine.execute_query("SELECT * FROM test_table")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], 'test')

if __name__ == '__main__':
    unittest.main()