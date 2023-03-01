from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.age = user['age']
        self.email = user['email']
        self.city = user['city']
        self.state = user['state']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']
        self.weights = []
        self.groups = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name,age,email,city,state, password) VALUES(%(first_name)s,%(last_name)s,%(age)s,%(email)s,%(city)s,%(state)s,%(password)s)"
        return connectToMySQL("Weights_With_Friends").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("Weights_With_Friends").query_db(query)
        user = []
        for x in results:
            user.append(cls(x))
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("Weights_With_Friends").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("Weights_With_Friends").query_db(query, data)
        print("results", (results))
        return cls(results[0])

    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("Weights_With_Friends").query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if not user["age"]:
            is_valid = False
            flash("Please enter an age!")
        if len(user['city']) < 3:
            flash("City must be at least 2 characters", "register")
            is_valid = False
        if len(user['state']) < 2:
            flash("State must be at least 2 characters", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Invalid email/password!", "register")
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email/password!", "register")
            is_valid = False
        return is_valid
