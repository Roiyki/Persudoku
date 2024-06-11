import os
import sys
import pytest
from pymongo import MongoClient

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.Backend.main import app

# Define the MongoDB URI for testing
TEST_MONGO_URI = 'mongodb://localhost:27017/sudoku_app_test'

@pytest.fixture
def client():
    # Set up the Flask app for testing
    app.testing = True
    app.config['MONGO_URI'] = TEST_MONGO_URI
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Set up the MongoDB test database connection
    client = MongoClient(TEST_MONGO_URI)
    db = client.get_database()
    users_collection = db.users
    
    # Clean up the test database before and after each test
    yield
    users_collection.delete_many({})

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 302  # Ensure it redirects

def test_generate_sudoku(client):
    response = client.post('/generate_sudoku', data={'difficulty': 'easy'})
    assert response.status_code == 200  # Ensure it returns successfully

def test_place_number(client):
    response = client.post('/place_number', data={'selected_number': '5', 'cell_index': '0'})
    assert response.status_code == 400  # Expecting a Bad Request status code

def test_registration(client):
    registration_data = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    }
    print("Your Registration Data:", registration_data)

    # Simulate a registration request
    response = client.post('/register', data=registration_data)

    # Print request data
    print("Registration Request Data:", response.request.data)

    # Print response status code and headers
    print("Registration Response Status Code:", response.status_code)
    print("Registration Response Headers:", response.headers)

    # Check if registration was successful
    assert response.status_code == 302  # Expecting a redirect status code
    assert response.headers['Location'] == '/login'  # Ensure it redirects to the relative login page