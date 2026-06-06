from flask import Blueprint, render_template, request
from models import db, Recipe, Category, Favorite

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Последние рецепты
    latest_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    
    # Популярные рецепты (по количеству добавлений в избранное)
    popular_recipes = db.session.query(Recipe).join(Favorite, Favorite.recipe_id == Recipe.id)\
        .group_by(Recipe.id).order_by(db.func.count(Favorite.recipe_id).desc()).limit(6).all()
    
    # Если популярных рецептов меньше 6, добираем последними
    if len(popular_recipes) < 6:
        remaining = 6 - len(popular_recipes)
        existing_ids = [r.id for r in popular_recipes]
        additional = Recipe.query.filter(~Recipe.id.in_(existing_ids)).order_by(Recipe.views_count.desc()).limit(
            remaining).all()
        popular_recipes.extend(additional)
    
    return render_template('index.html', latest_recipes=latest_recipes, popular_recipes=popular_recipes)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', 0, type=int)
    difficulty = request.args.get('difficulty', '')
    min_time = request.args.get('min_time', 0, type=int)
    max_time = request.args.get('max_time', 0, type=int)
    
    recipes = Recipe.query
    
    if query:
        recipes = recipes.filter(
            Recipe.title.contains(query) |
            Recipe.ingredients.contains(query) |
            Recipe.description.contains(query)
        )
    
    if category_id > 0:
        recipes = recipes.filter_by(category_id=category_id)
    
    if difficulty:
        recipes = recipes.filter_by(difficulty=difficulty)
    
    if min_time > 0:
        recipes = recipes.filter(Recipe.cooking_time >= min_time)
    
    if max_time > 0:
        recipes = recipes.filter(Recipe.cooking_time <= max_time)
    
    recipes = recipes.order_by(Recipe.created_at.desc()).all()
    categories = Category.query.all()
    
    return render_template('search_results.html', recipes=recipes, query=query, categories=categories)