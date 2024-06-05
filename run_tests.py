import os
import pytest

def run_tests():
    # Get the absolute path to the tests directory
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'tests')
    
    # Run pytest from the tests directory
    os.chdir(tests_dir)
    pytest.main()

if __name__ == "__main__":
    run_tests()
