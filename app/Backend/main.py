from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
import os
from urllib.parse import quote

# Set the path to the template folder
template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Frontend/templates"))
print("Template Folder:", template_folder)

# Initialize the Flask app with the correct template folder
app = Flask(__name__, template_folder=template_folder)

app.config['MONGO_URI'] = "mongodb://mongodb-service.mongodb-namespace.svc.cluster.local:27017/mydatabase"
mongo = PyMongo(app)

# Initialize the global grid and other variables
grid = [[0 for _ in range(9)] for _ in range(9)]
attempts_left = 3

# Check if a number can be placed in a position
def possible(row, column, number):
    global grid
    for i in range(0, 9):
        if grid[row][i] == number:
            return False
    for i in range(0, 9):
        if grid[i][column] == number:
            return False
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0+i][x0+j] == number:
                return False
    return True

# Solve the Sudoku using backtracking
def solve():
    global grid
    for row in range(0, 9):
        for column in range(0, 9):
            if grid[row][column] == 0:
                for number in range(1, 10):
                    if possible(row, column, number):
                        grid[row][column] = number
                        if solve():
                            return True
                        grid[row][column] = 0
                return False
    return True

# Check if the grid is solvable
def is_solvable():
    global grid
    original_grid = [row[:] for row in grid]
    solvable = solve()
    grid = original_grid
    return solvable

# Generate a full Sudoku grid
def generate_full_grid():
    global grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve()

# Remove cells to create a puzzle
def remove_cells(n):
    global grid
    count = n
    while count > 0:
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        while grid[row][column] == 0:
            row = random.randint(0, 8)
            column = random.randint(0, 8)
        backup = grid[row][column]
        grid[row][column] = 0

        if not is_solvable():
            grid[row][column] = backup
        else:
            count -= 1

# Access the database within the app context
def setup_database():
    global users_collection
    if not hasattr(app, 'mongo_client'):
        app.mongo_client = MongoClient(app.config['MONGO_URI'])
        app.db = app.mongo_client.get_database()
        users_collection = app.db.users

# Set up the home route
@app.route("/")
def home():
    template_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
    print("Template Folder Path:", template_folder_path)
    setup_database()
    return redirect(url_for('login'))

# Route to render the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    setup_database()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = users_collection.find_one({"email": email})
        
        if user and user["password"] == password:
            return render_template("index.html")  # Redirect to index.html
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

# Route to render the registration page and handle registration
@app.route("/register", methods=["GET", "POST"])
def register():
    setup_database()
    if request.method == "POST":
        if "full_name" in request.form and "email" in request.form and "password" in request.form:
            user_data = {
                "full_name": request.form["full_name"],
                "email": request.form["email"],
                "password": request.form["password"]
            }
            users_collection.insert_one(user_data)
            return redirect(url_for('login'))
        else:
            return "Bad Request: Missing required form fields", 400
    else:
        return render_template("register.html")

# Route to generate a Sudoku puzzle
@app.route("/generate", methods=["POST"])
def generate_sudoku():
    global grid, attempts_left
    difficulty = request.form.get("difficulty")
    print(f"Selected difficulty: {difficulty}")
    difficulties = {
        'easy': 30,
        'medium': 40,
        'hard': 50
    }
    if difficulty not in difficulties:
        print("Invalid difficulty level.")
        return "Invalid difficulty level."
    generate_full_grid()
    remove_cells(difficulties[difficulty])
    attempts_left = 3
    return render_template("sudoku.html", grid=grid, attempts_left=attempts_left, difficulty=difficulty)

# Route to place a number on the Sudoku grid
@app.route("/place-number", methods=["POST"])
def place_number():
    global grid, attempts_left
    selected_number = int(request.form.get("selected_number"))
    print("Selected Number:", selected_number)
    cell_index = request.form.get("cell_index")
    print("Cell Index:", cell_index)
    if selected_number < 1 or selected_number > 9:
        return jsonify({'status': 'error', 'message': 'Invalid number'})
    if not cell_index.isdigit() or int(cell_index) < 0 or int(cell_index) >= 81:
        return jsonify({'status': 'error', 'message': 'Invalid cell index'})
    row = int(cell_index) // 9
    column = int(cell_index) % 9
    if grid[row][column] != 0:
        return jsonify({'status': 'error', 'message': 'Cell is already filled'})
    if possible(row, column, selected_number):
        grid[row][column] = selected_number
        if all(all(cell != 0 for cell in row) for row in grid):  
            return jsonify({'status': 'win', 'message': 'Congratulations! You solved the puzzle!', 'correct': True})
        return jsonify({'status': 'success', 'message': 'Number placed successfully', 'correct': True})

    else:
        attempts_left -= 1
        if attempts_left <= 0:
            return jsonify({'status': 'lose', 'message': 'Game over! No attempts left.', 'correct': False})
        return jsonify({'status': 'error', 'message': f'Invalid placement. Attempts left: {attempts_left}', 'correct': False})

# Access the database
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()
users_collection = db.users

# Close the MongoClient after the last request is handled
@app.teardown_appcontext
def teardown_appcontext(error=None):
    if hasattr(app, 'mongo_client'):
        app.mongo_client.close()
        del app.mongo_client

@app.route("/test_db_connection", methods=["GET"])
def test_db_connection():
    try:
        user = users_collection.find_one()
        if user:
            return "Successfully connected to the MongoDB database and retrieved a document."
        else:
            return "Successfully connected to the MongoDB database, but no documents found."
    except Exception as e:
        return f"An error occurred while connecting to the MongoDB database: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
