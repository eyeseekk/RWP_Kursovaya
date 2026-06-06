from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Recipe, Comment, Favorite
from forms import ProfileForm
from utils import save_avatar, delete_file, allowed_file

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def index():
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.created_at.desc()).all()
    stats = {
        'recipes_count': len(user_recipes),
        'comments_count': Comment.query.filter_by(user_id=current_user.id).count(),
        'favorites_count': Favorite.query.filter_by(user_id=current_user.id).count()
    }
    return render_template('profile.html', user_recipes=user_recipes, stats=stats)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.avatar.data and allowed_file(form.avatar.data.filename):
            delete_file(current_user.avatar)
            avatar_path = save_avatar(form.avatar.data, current_user.id)
            if avatar_path:
                current_user.avatar = avatar_path
        
        db.session.commit()
        flash('Профиль обновлен!', 'success')
        return redirect(url_for('profile.index'))
    
    return render_template('profile_edit.html', form=form)