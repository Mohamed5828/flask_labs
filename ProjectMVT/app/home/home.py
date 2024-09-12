from flask import Flask, render_template, session, request, flash, redirect, url_for
from app.models import User, Book
from werkzeug.security import generate_password_hash
from app import db
from app.home import home_routes
from app.decorators import login_required , admin_required

@home_routes.route('/')
def home_page():
    # return render_template('/')
    pass

@home_routes.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('/profile.html', user=user, books=user.books)



@home_routes.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image = request.files['image'].read() if 'image' in request.files else None
        
        if 'admin' in session and session['admin']:
           
            new_book = Book(title=title, author=author, image=image)
        else:
            new_book = Book(title=title, author=author, image=image, user_id=session['user_id'])
        
        db.session.add(new_book)
        db.session.commit()
        
        flash("Book added successfully!")
        if 'admin' in session and session['admin']:
            return redirect(url_for('home.admin_dashboard'))
        else:
            return redirect(url_for('home.profile'))

    return render_template('add_book.html')

@home_routes.route('/delete-book/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book and book.owner.id == session['user_id']:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully!")
    else:
        flash("You do not have permission to delete this book!")
    return redirect(url_for('home.profile'))

@home_routes.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_dashboard.html', users=users, books=books)

@home_routes.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found!")
        return redirect(url_for('home.admin_dashboard'))
    
    if request.method == 'POST':
        user.username = request.form['username']
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'])
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash(f"User {user.username} updated successfully!")
        return redirect(url_for('home.admin_dashboard'))
    
    return render_template('admin_edit_user.html', user=user)

@home_routes.route('/admin/delete-user/<int:user_id>')
@admin_required
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted!")
    else:
        flash("User not found!")
    return redirect(url_for('home.admin_dashboard'))

@home_routes.route('/admin/edit-book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Book not found!")
        return redirect(url_for('home.admin_dashboard'))
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        if 'image' in request.files:
            book.image = request.files['image'].read()
        db.session.commit()
        flash(f"Book {book.title} updated successfully!")
        return redirect(url_for('home.admin_dashboard'))
    
    return render_template('admin_edit_book.html', book=book)

@home_routes.route('/admin/delete-book/<int:book_id>')
@admin_required
def admin_delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash(f"Book {book.title} deleted!")
    else:
        flash("Book not found!")
    return redirect(url_for('home.admin_dashboard'))

@home_routes.route('/view-books')
@login_required
def view_books():
    books = Book.query.all()
    return render_template('view_books.html', books=books)
