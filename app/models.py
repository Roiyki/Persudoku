#app/models.py
from flask_pymongo import PyMongo
import random
from . import mongo

grid = [[0 for _ in range(9)] for _ in range(9)]
attempts_left = 3

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

    grid_copy = [row[:] for row in grid]
    return solve(grid_copy)

def generate_full_grid():
    global grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve(grid)

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
            if not is_solvable_grid(grid):
                grid[row][col] = backup
            else:
                cells_to_remove -= 1

def setup_database():
    try:
        global users_collection
        users_collection = mongo.db.users
    except AttributeError as e:
        print(f"Failed to access MongoDB collection: {str(e)}")
        # Handle attribute error as needed
