from flask import Blueprint, render_template, flash, redirect, url_for, request
from apps.app import db
from apps.crud.models import User
from apps.auth.forms import SignUpForm
from flask_login import login_user

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static')


@auth.route('/')
def index():
    return render_template('auth/index.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplocate_email():
            flash('指定のメールは既に登録されています。')
            return redirect(url_for('auth.signup'))

        db.session.add(user)
        db.session.commit()
        login_user(user)
        next_ = request.args.get('next')
        if next_ is None or not next_.startswith('/'):
            next_ = url_for('crud.users')
        return redirect(next_)
    return render_template('auth/signup.html', form=form)
