#app/routes.py
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from .models import possible, solve, generate_full_grid, remove_cells, setup_database, grid, attempts_left
from . import mongo

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    setup_database()
    return redirect(url_for('main.login'))  # Correctly reference 'main.login'

@bp.route("/", methods=["POST"])
def handle_post_request():
    return redirect(url_for('main.login'))

@bp.route("/index")
def index():
    return render_template("main/index.html")

@bp.route("/explanation")
def explanation():
    return render_template("main/explanation.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    setup_database()
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            user = mongo.db.users.find_one({"email": email})
            if user and user["password"] == password:
                return jsonify({"redirect": url_for('main.index')})
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        except Exception as e:
            return jsonify({"message": f"Error occurred during login: {str(e)}"}), 500
    else:
        return render_template("main/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    setup_database()
    if request.method == "POST":
        try:
            if all(key in request.form for key in ["full_name", "email", "password"]):
                user_data = {
                    "full_name": request.form["full_name"],
                    "email": request.form["email"],
                    "password": request.form["password"]
                }
                mongo.db.users.insert_one(user_data)
                return redirect(url_for('main.login'))
            else:
                return jsonify({"message": "Bad Request: Missing required form fields"}), 400
        except Exception as e:
            return jsonify({"message": f"Error occurred during registration: {str(e)}"}), 500
    else:
        return render_template("main/register.html")  # Ensure the correct template name here

@bp.route("/generate_sudoku", methods=["POST"])
def generate_sudoku():
    global grid, attempts_left
    difficulty = request.form.get("difficulty")
    difficulties = {
        'easy': 50,
        'medium': 40,
        'hard': 30
    }
    if difficulty not in difficulties:
        return jsonify({"message": "Invalid difficulty level."}), 400
    generate_full_grid()
    remove_cells(difficulties[difficulty])
    attempts_left = 3
    return jsonify({"redirect": url_for('main.sudoku', difficulty=difficulty)})

@bp.route("/sudoku")
def sudoku():
    difficulty = request.args.get('difficulty', 'medium')
    return render_template("main/sudoku.html", grid=grid, attempts_left=attempts_left, difficulty=difficulty)

@bp.route("/place_number", methods=["POST"])
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

@bp.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@bp.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized", "message": str(error)}), 401

@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@bp.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405

@bp.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
