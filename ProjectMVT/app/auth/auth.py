from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.auth import auth_routes





@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        is_admin = 'is_admin' in request.form
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('auth.signup'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists!")
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please login.")
        return redirect(url_for('auth.login'))

    return render_template('/signup.html')

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully!")
            return redirect(url_for('home.profile'))
        else:
            flash("Invalid credentials!")
            return redirect(url_for('auth.login'))

    return render_template('/login.html')

@auth_routes.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!")
    return redirect(url_for('auth.login'))
