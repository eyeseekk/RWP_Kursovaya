import os

class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    
    # PostgreSQL
    DB_USER = 'postgres'
    DB_PASSWORD = 'Morendi16'  # Замените на ваш пароль
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'cooking_db'
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки загрузки файлов
    UPLOAD_FOLDER_AVATARS = 'static/uploads/avatars'
    UPLOAD_FOLDER_RECIPES = 'static/uploads/recipes'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @staticmethod
    def init_directories():
        os.makedirs('static/uploads/avatars', exist_ok=True)
        os.makedirs('static/uploads/recipes', exist_ok=True)