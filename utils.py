import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
import uuid


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_avatar(file, user_id):
    if not file or file.filename == '':
        return None

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"user_{user_id}.{ext}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_AVATARS'], filename)

    # Обработка изображения
    img = Image.open(file)
    img = img.resize((200, 200), Image.LANCZOS)

    # Сохранение с оптимизацией
    if ext in ['jpg', 'jpeg']:
        img.save(filepath, 'JPEG', quality=85, optimize=True)
    elif ext == 'png':
        img.save(filepath, 'PNG', optimize=True)
    elif ext == 'webp':
        img.save(filepath, 'WEBP', quality=85)
    else:
        img.save(filepath)

    return f"uploads/avatars/{filename}"


def save_recipe_image(file, recipe_id):
    if not file or file.filename == '':
        return None

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"recipe_{recipe_id}.{ext}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_RECIPES'], filename)

    # Обработка изображения
    img = Image.open(file)
    # Изменение размера с сохранением пропорций
    img.thumbnail((800, 600), Image.LANCZOS)

    if ext in ['jpg', 'jpeg']:
        img.save(filepath, 'JPEG', quality=85, optimize=True)
    elif ext == 'png':
        img.save(filepath, 'PNG', optimize=True)
    elif ext == 'webp':
        img.save(filepath, 'WEBP', quality=85)
    else:
        img.save(filepath)

    return f"uploads/recipes/{filename}"


def delete_file(filepath):
    if filepath and not filepath.endswith('default.png') and not filepath.endswith('placeholder.png'):
        full_path = os.path.join('static', filepath)
        if os.path.exists(full_path):
            os.remove(full_path)