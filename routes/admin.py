from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Category

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/categories')
@login_required
def categories():
    if not current_user.is_admin():
        abort(403)
    
    categories = Category.query.all()
    return render_template('admin_categories.html', categories=categories)

@admin_bp.route('/category/new', methods=['POST'])
@login_required
def new_category():
    if not current_user.is_admin():
        abort(403)
    
    name = request.form.get('name')
    slug = request.form.get('slug')
    
    if name and slug:
        category = Category(name=name, slug=slug)
        db.session.add(category)
        db.session.commit()
        flash('Категория добавлена', 'success')
    
    return redirect(url_for('admin.categories'))

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin():
        abort(403)
    
    category = Category.query.get_or_404(category_id)
    if category.recipes:
        flash('Нельзя удалить категорию, содержащую рецепты', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Категория удалена', 'success')
    
    return redirect(url_for('admin.categories'))