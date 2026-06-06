from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Имя пользователя уже занято')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email уже зарегистрирован')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Краткое описание', validators=[DataRequired()])
    ingredients = TextAreaField('Ингредиенты', validators=[DataRequired()])
    steps = TextAreaField('Шаги приготовления', validators=[DataRequired()])
    cooking_time = IntegerField('Время приготовления (мин)', validators=[DataRequired(), NumberRange(min=1, max=600)])
    difficulty = SelectField('Сложность', choices=[
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно')
    ], validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])
    image = FileField('Фото блюда',
                      validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Только изображения!')])
    submit = SubmitField('Сохранить рецепт')


class CommentForm(FlaskForm):
    content = TextAreaField('Комментарий', validators=[DataRequired(), Length(max=2000)])
    rating = SelectField('Оценка',
                         choices=[('', 'Без оценки'), ('5', '★★★★★'), ('4', '★★★★☆'), ('3', '★★★☆☆'), ('2', '★★☆☆☆'),
                                  ('1', '★☆☆☆☆')])
    submit = SubmitField('Отправить')


class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Только изображения!')])
    submit = SubmitField('Сохранить изменения')