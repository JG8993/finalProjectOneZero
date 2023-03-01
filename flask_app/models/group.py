from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Group:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.creator = None

    @classmethod
    def get_all_groups_with_creator(cls):  # this will be used on dashboard
        query = "SELECT * FROM my_group JOIN users on my_group.user_id = users.id;"
        results = connectToMySQL('Weights_With_Friends').query_db(query)
        all_groups = []
        for x in results:
            one_group = cls(x)
            one_groups_creator_info = {
                "id": x['users.id'],
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
            author = User(one_groups_creator_info)
            one_group.creator = author
            all_groups.append(one_group)
        return all_groups

    @classmethod
    def save_group(cls, data):  # this will be used on creategroup.html
        query = "INSERT INTO my_group (name,user_id) VALUES (%(name)s,%(user_id)s)"
        return connectToMySQL("Weights_With_Friends").query_db(query, data)

    @classmethod
    def get_group_by_id(cls, data):
        query = "SELECT * FROM my_group WHERE id = %(id)s;"
        results = connectToMySQL('Weights_With_Friends').query_db(query, data)
        print("results", (results))
        return cls(results[0])

    @classmethod
    def user_join_group(cls, data):
        query = "INSERT INTO users_join_group (my_group_id, users_id) SELECT my_group.id, users.id FROM my_group JOIN users WHERE my_group.id = %(my_group_id)s AND users.id = %(users_id)s;"
        return connectToMySQL('Weights_With_Friends').query_db(query, data)


#        query = "SELECT u.first_name, g.* FROM users u JOIN my_group g ON u.id = g.user_id"
#        query = "SELECT users.first_name FROM users INNER JOIN my_group ON users.id = my_group.user_id WHERE my_group.name =  %(id)s;"
#       query = "SELECT my_group.name, users.first_name FROM users INNER JOIN my_group ON users.id = my_group.user_id WHERE my_group.name = %(id)s;"
