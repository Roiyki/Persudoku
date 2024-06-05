import pytest

def run_tests():
    # Run pytest from the current directory, specifying the root directory where tests are located
    pytest.main(['--rootdir=root/Persudoku/app/tests'])

if __name__ == "__main__":
    run_tests()
