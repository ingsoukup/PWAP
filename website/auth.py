from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Uživatel úspěšně přihlášen', category='success')
                login_user(user, remember=True) #user je ulozen ve flask session
                return redirect(url_for('views.home'))
            else: 
                flash('Neúspěšné přihlášení, opakujte pokus znovu', category='error')
        else:
            flash('Email nenalezen', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required #route je pristupna pouze pokud je uzivatel prihlasen
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email je již zaregistrovaný', category='error')
        elif len(email)<4:
            flash('Email musí být delší než 4 znaky', category='error')
        elif len(first_name)<2:
            flash('Jméno musí být delší než 2 znaky', category='error')
        elif len(password1)<7:
            flash('Heslo musí mít alespoň 8 znaků', category='error')
        elif password1 != password2:
            flash('Hesla nesouhlasí', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) #user je ulozen ve flask session
            flash('Uživatel vytvořen!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

