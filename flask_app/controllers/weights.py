from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.weight import Weight
from flask_app.models.user import User
from flask_app.controllers import users
from flask_app.models.group import Group


@app.route('/create_weight_page/<int:id>')
def create_weight_page(id):
    data = {
        "id": id
    }
    return render_template("addnew.html", group=Group.get_group_by_id(data))


@app.route('/add_new_weight', methods=['POST'])
def add_new_weight():

    if not Weight.validate_weight(request.form):
        return redirect('/create_car_page')
    data = {
        "exercise": request.form['exercise'],
        "weight_lifted": request.form['weight_lifted'],
        "current_bodyweight": request.form['current_bodyweight'],
        "user_id": session['user_id'],
        "my_group_id": request.form['my_group_id']
    }
    Weight.save_weight(data)
    return redirect('/success')


@app.route("/show_weight/<int:id>")
def show_weight(id):
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("show.html", user=User.get_by_id(user_data), weights=Weight.get_one_weight_with_creator(data))


@app.route("/edit_weight/<int:id>")
def edit_weight(id):
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("edit.html", weights=Weight.get_one_weight(data), user=User.get_by_id(user_data))


@app.route('/update', methods=["POST"])
def update():
    if not Weight.validate_weight(request.form):
        return redirect(f"/edit_car/{request.form['id']}")
    data = {
        "exercise": request.form['exercise'],
        "weight_lifted": request.form["weight_lifted"],
        "current_bodyweight": request.form['current_bodyweight'],
        "id": request.form["id"]
    }
    Weight.edit_weight(data)
    return redirect('/success')


@app.route('/delete_weight/<int:id>')
def delete_weight(id):
    data = {
        "id": id
    }
    Weight.delete_weight(data)
    return redirect('/success')


def calculate_plates_weight(target_weight, bar_weight=45, plate_weights=[45, 35, 25, 10, 5, 2.5]):

    plate_weight = (target_weight - bar_weight) / 2

    plates_per_side = {}

    for weight in plate_weights:
        if plate_weight >= weight:
            plates = int(plate_weight // weight)
            plates_per_side[weight] = plates
            plate_weight -= plates * weight

    return plates_per_side


@app.route('/calculate/<int:id>', methods=['POST'])
def calculate(id):
    target_weight = float(request.form['weight'])

    plates_per_side = calculate_plates_weight(target_weight)

    return render_template('weightresult.html', target_weight=target_weight, plates_per_side=plates_per_side, id=id)
