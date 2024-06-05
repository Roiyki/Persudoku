import os
import pytest

# Run the tests
def run_tests():
    # Change directory to the tests directory
    os.chdir("app/tests")

    # Run the tests with pytest
    pytest.main()

# Entry point for running tests
if __name__ == "__main__":
    run_tests()