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
# app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://mongo-service.mongo-namespace:27017/sudoku_app')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/sudoku_app_test')
mongo = PyMongo(app)  # Initialize PyMongo instance

# Initialize the global grid and other variables
grid = [[0 for _ in range(9)] for _ in range(9)]
attempts_left = 3

# Check if a number can be placed in a position
def possible(row, column, number):
    global grid
    for i in range(0, 9):
        if grid[row][i] == number or grid[i][column] == number:
            return False
    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0+i][x0+j] == number:
                return False
    return True

# Solve the Sudoku using backtracking
def solve(grid):
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                for number in range(1, 10):
                    if possible(row, column, number):
                        grid[row][column] = number
                        if solve(grid):
                            return True
                        grid[row][column] = 0
                return False
    return True

# Check if the grid is solvable
def is_solvable_grid(grid):
    def solve(grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == 0:
                    for number in range(1, 10):
                        if possible(row, column, number):
                            grid[row][column] = number
                            if solve(grid):
                                return True
                            grid[row][column] = 0
                    return False
        return True

    # Create a deep copy of the grid to avoid modifying the original grid
    grid_copy = [row[:] for row in grid]
    return solve(grid_copy)

# Generate a full Sudoku grid
def generate_full_grid():
    global grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve(grid)

# Remove cells to create a puzzle
def remove_cells(n):
    global grid
    cells_to_remove = 81 - n
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    for pos in positions:
        row, col = pos
        if cells_to_remove <= 0:
            break
        if grid[row][col] != 0:
            backup = grid[row][col]
            grid[row][col] = 0

            # Check if the modified grid is still solvable
            if not is_solvable_grid(grid):
                grid[row][col] = backup
            else:
                cells_to_remove -= 1


# Access the database within the app context
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

@app.route("/", methods=["POST"])
def handle_post_request():
    # Handle the POST request here
    # Redirect to the login page after processing the request
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
                return jsonify({"redirect": url_for('index')})
            else:
                print("Invalid credentials")
                return jsonify({"message": "Invalid credentials"}), 401
        except Exception as e:
            print("Error occurred during login:", e)
            return jsonify({"message": f"Error occurred during login: {str(e)}"}), 500
    elif request.method == "GET":
        # Return the login form for GET requests
        return render_template("login.html")
    else:
        return jsonify({"message": "Method not allowed"}), 405

# Route to render the registration page and handle registration
@app.route("/register", methods=["GET", "POST"])
def register():
    setup_database()  # Ensure the database is set up
    print(f"Request Method: {request.method}, URL: {request.url}")

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
    print(f"Request Method: {request.method}, URL: {request.url}")
    difficulty = request.form.get("difficulty")
    print(f"Selected difficulty: {difficulty}")
    difficulties = {
        'easy': 50,
        'medium': 40,
        'hard': 30
    }
    if difficulty not in difficulties:
        print("Invalid difficulty level.")
        return jsonify({"message": "Invalid difficulty level.."}), 400
    generate_full_grid()
    remove_cells(difficulties[difficulty])
    attempts_left = 3
    return jsonify({"redirect": url_for('sudoku', difficulty=difficulty)})

@app.route("/sudoku")
def sudoku():
    difficulty = request.args.get('difficulty', 'medium')  # Default to medium if not provided
    return render_template("sudoku.html", grid=grid, attempts_left=attempts_left, difficulty=difficulty)

# Route to place a number on the Sudoku grid
@app.route("/place_number", methods=["POST"])
def place_number():
    global grid, attempts_left
    print(f"Request Method: {request.method}, URL: {request.url}")
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
    print(f"400 Error: {error}")
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

# Error handler for 401 Unauthorized errors
@app.errorhandler(401)
def unauthorized_error(error):
    print(f"401 Error: {error}")
    return jsonify({"error": "Unauthorized", "message": str(error)}), 401

# Error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    print(f"404 Error: {error}")
    return jsonify({"error": "Not Found", "message": str(error)}), 404

# Error handler for 405 Method Not Allowed errors
@app.errorhandler(405)
def method_not_allowed_error(error):
    print(f"405 Error: {error}")
    return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405

# Error handler for 500 Internal Server Error errors
@app.errorhandler(500)
def internal_server_error(error):
    print(f"500 Error: {error}")
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
