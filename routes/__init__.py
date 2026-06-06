from flask import Blueprint
from routes.main import main_bp
from routes.auth import auth_bp
from routes.recipes import recipes_bp
from routes.profile import profile_bp
from routes.admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')