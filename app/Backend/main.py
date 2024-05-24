from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_pymongo import PyMongo
import random
import os

# Set the path to the template folder
template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates"))
print("Template Folder:", template_folder)

# Initialize the Flask app with the correct template folder
app = Flask(__name__, template_folder=template_folder)

# Update MongoDB URI to use the Docker service name
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://mongodb:27017/sudoku_app')

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
@app.before_first_request
def setup_database():
    global users_collection
    users_collection = mongo.db.users

# Set up the home route
@app.route("/")
def home():
    template_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
    print("Template Folder Path:", template_folder_path)
    setup_database()
    return redirect(url_for('login'))

# Route to serve index.html
@app.route("/index")
def index():
    return render_template("index.html")

# Route to render the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    setup_database()
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            print("Received email:", email)
            print("Received password:", password)
            
            user = users_collection.find_one({"email": email})
            if user and user["password"] == password:
                print("User found and password matched")
                # Redirect to index.html after successful login
                return redirect(url_for('index'))  
            else:
                print("Invalid credentials")
                return jsonify({"message": "Invalid credentials"}), 401
        except Exception as e:
            print("Error occurred during login:", e)
            return jsonify({"message": f"Error occurred during login: {str(e)}"}), 500
    return render_template("login.html")

# Route to render the registration page and handle registration
@app.route("/register", methods=["GET", "POST"])
def register():
    setup_database()  # Ensure the database is set up

    if request.method == "POST":
        try:
            # Check if all required form fields are present
            if all(key in request.form for key in ["full_name", "email", "password"]):
                user_data = {
                    "full_name": request.form["full_name"],
                    "email": request.form["email"],
                    "password": request.form["password"]
                }
                # Insert user data into the MongoDB collection
                users_collection.insert_one(user_data)
                return redirect(url_for('login'))
            else:
                # Return a 400 Bad Request response if any required field is missing
                return jsonify({"message": "Bad Request: Missing required form fields"}), 400
        except Exception as e:
            # Return a 500 Internal Server Error response if any exception occurs
            return jsonify({"message": f"Error occurred during registration: {str(e)}"}), 500
    else:
        # Render the registration page for GET requests
        return render_template("register.html")

# Route to generate a Sudoku puzzle
@app.route("/generate_sudoku", methods=["POST"])
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
        return jsonify({"message": "Invalid difficulty level."}), 400
    generate_full_grid()
    remove_cells(difficulties[difficulty])
    attempts_left = 3
    return render_template("sudoku.html", grid=grid, attempts_left=attempts_left, difficulty=difficulty)


# Route to place a number on the Sudoku grid
@app.route("/api/place_number", methods=["POST"])
def place_number():
    global grid, attempts_left
    selected_number = int(request.form.get("selected_number"))
    cell_index = request.form.get("cell_index")
    try:
        if selected_number < 1 or selected_number > 9:
            return jsonify({"message": "Invalid number"}), 400
        if not cell_index.isdigit() or int(cell_index) < 0 or int(cell_index) >= 81:
            return jsonify({"message": "Invalid cell index"}), 400
        row = int(cell_index) // 9
        column = int(cell_index) % 9
        if grid[row][column] != 0:
            return jsonify({"message": "Cell is already filled"}), 400
        if possible(row, column, selected_number):
            grid[row][column] = selected_number
            if all(all(cell != 0 for cell in row) for row in grid):  
                return jsonify({"message": "Congratulations! You solved the puzzle!", "correct": True})
            return jsonify({"message": "Number placed successfully", "correct": True})
        else:
            attempts_left -= 1
            if attempts_left <= 0:
                return jsonify({"message": "Game over! No attempts left.", "correct": False}), 400
            return jsonify({"message": f"Invalid placement. Attempts left: {attempts_left}", "correct": False}), 400
    except Exception as e:
        return jsonify({"message": f"Error occurred during number placement: {str(e)}"}), 500

# Error handler for 400 Bad Request errors
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

# Error handler for 401 Unauthorized errors
@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401

# Error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found on the server"}), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred on the server"}), 500

# Close the MongoClient after the last request is handled
@app.teardown_appcontext
def teardown_appcontext(error=None):
    if hasattr(app, 'mongo') and app.mongo.cx:
        try:
            app.mongo.cx.close()
        except Exception as e:
            app.logger.error(f"An error occurred while closing the MongoDB client connection: {e}")
        finally:
            del app.mongo

@app.route("/test_db_connection", methods=["GET"])
def test_db_connection():
    try:
        user = mongo.db.users.find_one()
        if user:
            return "Successfully connected to the MongoDB database and retrieved a document."
        else:
            return "Successfully connected to the MongoDB database, but no documents found."
    except Exception as e:
        return f"An error occurred while connecting to the MongoDB database: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

