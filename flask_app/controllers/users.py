from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.weight import Weight
from flask_app.models.group import Group
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():

    if not User.validate(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age": request.form['age'],
        "email": request.form['email'],
        "city": request.form['city'],
        "state": request.form['state'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    session['first_name'] = data['first_name']

    return redirect('/success')


@app.route('/login', methods=['POST'])
def success_login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/success')


@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), groups=Group.get_all_groups_with_creator())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
