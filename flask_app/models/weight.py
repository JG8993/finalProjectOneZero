from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.group import Group
from flask import flash


class Weight:
    def __init__(self, data):
        self.id = data['id']
        self.exercise = data['exercise']
        self.weight_lifted = data['weight_lifted']
        self.current_bodyweight = data['current_bodyweight']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.group_id = data['my_group_id']

    @classmethod
    def get_all_weights_with_creator(cls):
        # edit query to display last 3 entries
        query = "SELECT * FROM weights JOIN users on weights.user_id = users.id;"
        results = connectToMySQL('Weights_With_Friends').query_db(query)
        all_weights = []
        for x in results:
            one_weight = cls(x)
            one_weights_creator_info = {
                "id": x['users.id'],
                "group_id": x["my_group_id"],
                "first_name": x['first_name'],
                "last_name": x['last_name'],
                "age": x['age'],
                "email": x['email'],
                "city": x['city'],
                "state": x['state'],
                "password": x['password'],
                "created_at": x['users.created_at'],
                "updated_at": x['users.updated_at']
            }
            author = User(one_weights_creator_info)
            one_weight.creator = author
            all_weights.append(one_weight)
        return all_weights

    @classmethod
    def get_all_weights(cls):
        query = "SELECT * FROM weights;"
        results = connectToMySQL('Weights_With_Friends').query_db(query)
        weights = []
        for x in results:
            weights.append(cls(x))
        return weights

    @classmethod
    def get_one_weight_with_creator(cls, data):
        query = "SELECT * FROM users join weights ON users.id = weights.user_id WHERE weights.id = %(id)s;"
        results = connectToMySQL('Weights_With_Friends').query_db(query, data)
        one_weight = cls(results[0])
        # creator is usually none, but we update to be the first_name
        one_weight.creator = results[0]["first_name"] + \
            " " + results[0]["last_name"]
        print(results[0])
        return one_weight

    @classmethod
    def save_weight(cls, data):
        query = "INSERT INTO weights (exercise,weight_lifted,current_bodyweight,user_id,my_group_id) VALUES (%(exercise)s,%(weight_lifted)s,%(current_bodyweight)s,%(user_id)s,%(my_group_id)s);"
        return connectToMySQL("Weights_With_Friends").query_db(query, data)

    @classmethod
    def get_one_weight(cls, data):
        query = "SELECT * FROM weights WHERE id = %(id)s;"
        results = connectToMySQL("Weights_With_Friends").query_db(query, data)
        return cls(results[0])

    @classmethod
    def edit_weight(cls, data):
        query = "UPDATE weights SET exercise= %(exercise)s,weight_lifted=%(weight_lifted)s, current_bodyweight= %(current_bodyweight)s WHERE id= %(id)s;"
        return connectToMySQL('Weights_With_Friends').query_db(query, data)

    @classmethod
    def delete_weight(cls, data):
        query = "DELETE FROM weights WHERE weights.id = %(id)s;"
        return connectToMySQL("Weights_With_Friends").query_db(query, data)

    @classmethod
    def get_all_weights_with_group(cls):
        query = "SELECT * FROM weights JOIN my_group on weights.mygroup_id = my_group.id;"
        results = connectToMySQL('Weights_With_Friends').query_db(query)
        all_weights = []
        for x in results:
            one_weight = cls(x)
            one_weights_group_info = {
                "id": x['my_group.id'],
                "name": x['name'],
                "created_at": x['created_at'],
                "updated_at": x['updated_at'],
            }
            group = Group(one_weights_group_info)
            one_weight.creator = group
            all_weights.append(one_weight)
        return all_weights

    @staticmethod
    def validate_weight(weight):
        is_valid = True
        if len(weight['exercise']) < 3:
            is_valid = False
            flash("Exercise must be at least 3 characters")
        if len(weight["weight_lifted"]) < 3:
            is_valid = False
            flash("Weighted Lifted must be at least 3 characters")
        if len(weight["current_bodyweight"]) < 2:
            is_valid = False
            flash("Current Bodyweight must be at least 2 characters")
        return is_valid
