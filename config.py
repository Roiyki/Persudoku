#config.py
import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/sudoku_app')
    TEMPLATE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/templates"))
