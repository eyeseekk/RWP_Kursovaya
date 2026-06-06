from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, make_response
from flask_login import login_required, current_user
from models import db, Recipe, Comment, Favorite, Category
from forms import RecipeForm, CommentForm
from utils import save_recipe_image, delete_file, allowed_file
from weasyprint import HTML

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/<int:recipe_id>')
def detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.views_count += 1
    db.session.commit()
    
    form = CommentForm()
    comments = Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favorite.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first() is not None
    
    return render_template('recipe_detail.html', recipe=recipe, form=form, comments=comments, is_favorited=is_favorited)

@recipes_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = RecipeForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            steps=form.steps.data,
            cooking_time=form.cooking_time.data,
            difficulty=form.difficulty.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.flush()
        
        if form.image.data and allowed_file(form.image.data.filename):
            image_path = save_recipe_image(form.image.data, recipe.id)
            if image_path:
                recipe.image = image_path
        
        db.session.commit()
        flash('Рецепт успешно создан!', 'success')
        return redirect(url_for('recipes.detail', recipe_id=recipe.id))
    
    return render_template('recipe_form.html', form=form, title='Новый рецепт')

@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = RecipeForm(obj=recipe)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.steps = form.steps.data
        recipe.cooking_time = form.cooking_time.data
        recipe.difficulty = form.difficulty.data
        recipe.category_id = form.category_id.data
        
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            if allowed_file(form.image.data.filename):
                delete_file(recipe.image)
                image_path = save_recipe_image(form.image.data, recipe.id)
                if image_path:
                    recipe.image = image_path
        
        db.session.commit()
        flash('Рецепт обновлен!', 'success')
        return redirect(url_for('recipes.detail', recipe_id=recipe.id))
    
    return render_template('recipe_form.html', form=form, title='Редактирование рецепта')

@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    delete_file(recipe.image)
    db.session.delete(recipe)
    db.session.commit()
    flash('Рецепт удален', 'success')
    return redirect(url_for('main.index'))

@recipes_bp.route('/<int:recipe_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    favorite = Favorite.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if favorite:
        db.session.delete(favorite)
        flash('Рецепт удален из избранного', 'info')
    else:
        favorite = Favorite(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(favorite)
        flash('Рецепт добавлен в избранное', 'success')
    
    db.session.commit()
    return redirect(url_for('recipes.detail', recipe_id=recipe_id))

@recipes_bp.route('/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            rating=int(form.rating.data) if form.rating.data else None,
            user_id=current_user.id,
            recipe_id=recipe_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен!', 'success')
    
    return redirect(url_for('recipes.detail', recipe_id=recipe_id))

@recipes_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    recipe_id = comment.recipe_id
    db.session.delete(comment)
    db.session.commit()
    flash('Комментарий удален', 'success')
    return redirect(url_for('recipes.detail', recipe_id=recipe_id))

@recipes_bp.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.created_at.desc()).all()
    return render_template('favorites.html', favorites=favorites)

@recipes_bp.route('/<int:recipe_id>/export')
@login_required
def export_pdf(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    rendered_html = render_template('recipe_pdf.html', recipe=recipe)
    pdf_file = HTML(string=rendered_html).write_pdf()
    
    response = make_response(pdf_file)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=recipe_{recipe.id}.pdf'
    return response