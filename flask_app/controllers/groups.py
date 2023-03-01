from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.weight import Weight
from flask_app.models.group import Group


@app.route('/create_group_page')
def create_group_page():
    return render_template("creategroup.html")


@app.route('/add_new_group', methods=['POST'])
def add_new_group():
    data = {
        "name": request.form['name'],
        "user_id": session['user_id']
    }
    Group.save_group(data)
    return redirect('/success')


# @app.route('/join_group', methods=['POST'])
# def join_group():

@app.route('/join_group_page/<int:id>')
def join_group_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id'],
    }
    data = {
        "id": id,
    }
    return render_template('joingroup.html', user=User.get_by_id(user_data), groups=Group.get_group_by_id(data))
# in form, id is pulling from groups.id


@app.route('/join_group/<int:id>', methods=['POST'])
def join_group(id):
    data = {
        "my_group_id": id,  # id is coming from join_group route
        # with this, you don't need hidden input. has to match to session.
        "users_id": session["user_id"]
    }
    Group.user_join_group(data)
    return redirect('/success')


@app.route('/show_group/<int:id>')  # display button
def show_groups(id):
    data = {
        "id": id
    }
    users = {}
    results = Weight.get_all_weights_with_creator()
    group_results = []
    for result in results:
        name = result.creator.id
        if result.group_id == id:
            if name in users and users[name] != 3:
                users[name] += 1
                group_results.append(result)
            elif name not in users:
                users[name] = 1
                group_results.append(result)

    return render_template('viewgroupstats.html', groups=Group.get_group_by_id(data), weight=group_results)
