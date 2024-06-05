import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.Backend.main import app

@pytest.fixture
def client():
    # Set up the Flask app for testing
    app.testing = True
    with app.test_client() as client:
        yield client

# Set up environment variable for MongoDB URI before running tests
@pytest.fixture(scope='session', autouse=True)
def set_mongo_uri():
    os.environ['MONGO_URI'] = 'mongodb://localhost:27017/sudoku_app_test'

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
    # Simulate a registration request
    response = client.post('/register', data={
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })

    # Check if registration was successful
    assert response.status_code == 302  # Expecting a redirect status code
    assert response.headers['Location'] == '/login'  # Ensure it redirects to the relative login page
