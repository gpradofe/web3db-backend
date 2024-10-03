import unittest
import sys

if __name__ == '__main__':
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('src/tests', pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero status if there were failures
    sys.exit(not result.wasSuccessful())