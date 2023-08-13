import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# メール設定
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

toolbar = DebugToolbarExtension(app)
mail = Mail(app)
print("Debug mode:", app.debug)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/contact')
def contact():
    responce = make_response(render_template('contact.html'))
    responce.set_cookie('flaskbook key', 'flaskbook value')
    session['username'] = 'yo'
    return responce


@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
    if request.method == 'POST':
        # 入力値のバリデーション
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        is_valid = True

        if not username:
            is_valid = False
            flash('名前を入力してください')
        if not email:
            is_valid = False
            flash('メールアドレスを入力してください')
        try:
            validate_email(email)
        except EmailNotValidError:
            is_valid = False
            flash('メールアドレスが不正です')
        if not description:
            is_valid = False
            flash('お問い合わせ内容を入力してください')

        if not is_valid:
            return redirect(url_for('contact'))

        # メール送信
        send_email(
            email,
            'お問い合わせありがとうございます',
            'contact_mail',
            username=username,
            description=description,
        )

        flash("お問い合わせをメールで送信しました")

        return redirect(url_for('contact_complete'))
    return render_template('contact_complete.html')


def send_email(to, subject, template, **kwargs):
    # メール送信
    msg = Message(
        subject,
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
