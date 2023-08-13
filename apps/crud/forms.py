from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class UserForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(
        message='必須項目です'), Length(max=30, message='30文字以内で入力してください')])
    email = StringField('メールアドレス', validators=[DataRequired(
        message='必須項目です'), Email(message='メールアドレスの形式で入力してください')])
    password = PasswordField('パスワード', validators=[
                             DataRequired(message='必須項目です')])

    submit = SubmitField('登録')
