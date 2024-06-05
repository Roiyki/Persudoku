import os
import pytest

def run_tests():
    # Get the absolute path to the app directory
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
    
    # Change the current working directory to the app directory
    os.chdir(app_dir)
    
    # Run pytest from the app directory
    pytest.main()

if __name__ == "__main__":
    run_tests()
