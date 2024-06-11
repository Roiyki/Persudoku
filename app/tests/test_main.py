import os
import sys
import pytest
from pymongo import MongoClient

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.Backend.main import app

# Define the MongoDB URI for testing
TEST_MONGO_URI = 'mongodb://mongo-service.mongo-namespace:27017/sudoku_app'  # Update URI to use Docker service name

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
    response = client.post('/register', data=registration_data, content_type='application/x-www-form-urlencoded')

    # Print request data (commented out because it causes issues)
    # print("Registration Request Data:", response.request.data)

    # Print response status code and headers
    print("Registration Response Status Code:", response.status_code)
    print("Registration Response Headers:", response.headers)

    # Check if registration was successful
    assert response.status_code == 302  # Expecting a redirect status code
    assert response.headers['Location'] == '/login'  # Ensure it redirects to the relative login page

def test_registration_another_user(client):
    registration_data = {
        'full_name': 'Another User',
        'email': 'anotheruser@example.com',
        'password': 'anotherpassword123'
    }

    # Simulate a registration request for another user
    response = client.post('/register', data=registration_data)

    # Check if registration was successful
    assert response.status_code == 302  # Expecting a redirect status code
    assert response.headers['Location'] == '/login'  # Ensure it redirects to the relative login page

    # Ensure that the user data is stored in the database
    client = MongoClient(TEST_MONGO_URI)  # Reconnect to the MongoDB using the test URI
    db = client.get_database()
    user = db.users.find_one({'email': 'anotheruser@example.com'})  # Access the users collection
    assert user is not None
    assert user['full_name'] == 'Another User'
    assert user['email'] == 'anotheruser@example.com'
    # Ensure the password is hashed or stored securely in the database
    # For this test, you can check if the password matches the expected value
    assert user['password'] == 'anotherpassword123'  # This line should be updated based on how passwords are stored in the database
