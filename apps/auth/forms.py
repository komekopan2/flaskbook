from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class SignUpForm(FlaskForm):
    username = StringField(
        'ユーザー名', validators=[
            DataRequired("必須項目です"),
            Length(1, 30, "30文字以内で入力してください"),
        ])
    email = StringField(
        'メールアドレス', validators=[
            DataRequired("必須項目です"),
            Email("メールアドレスの形式で入力してください"),
        ])
    password = PasswordField(
        'パスワード', validators=[
            DataRequired("必須項目です"),
        ])
    submit = SubmitField('新規登録')
