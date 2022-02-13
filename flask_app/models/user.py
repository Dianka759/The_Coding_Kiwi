from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# pass_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')



class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.email = data['email']
        self.role = data['role']
        self.summary = data['summary']
        self.instructor = data['instructor']
        self.students = data['students']
        self.current_stack = data['current_stack']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.photo = data['photo']


    @staticmethod
    def validate(user):        
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False

        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False

        if len(user["role"]) <= 0:
            flash("Must specify a role.", "register")
            is_valid = False

        if not email_regex.match(user['email']) : 
            flash("Invalid, Please provide a legit email address!", "register")
            is_valid = False
        else:
            email_check = connectToMySQL("website_schema")
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                "email": request.form["email"]
            }
            result = email_check.query_db(query, data)
            if result != ():
                flash("Email already exists, please enter a new email", "register")
                is_valid = False

        # if not pass_regex.match(user["password"]):
        #     flash("Password must be minimum 8 characters, at least one letter and one number.", "register")
        #     is_valid = False

        if len(user["password"]) < 3:
            flash("Password must be minimum 3 characters.", "register")
            is_valid = False

        if user['confirm_password'] != user['password']:
            flash("Passwords don't match!", "register")
            is_valid = False
        return is_valid



    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, role, email, password) VALUES (%(first_name)s, %(last_name)s, %(role)s, %(email)s, %(password)s)"
        return connectToMySQL("website_schema").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("website_schema").query_db(query,data)
        if len(user_db) < 1:
            return False
        return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(user_id)s"
        user_db = connectToMySQL("website_schema").query_db(query,data)
        return cls(user_db[0])

    @classmethod
    def get_users(cls,data):
        query = "SELECT * FROM users WHERE id=%(user_id)s"
        return connectToMySQL("website_schema").query_db(query,data)

    @classmethod
    def update_student(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password= %(password)s, birthday=%(birthday)s, gender=%(gender)s, instructor= %(instructor)s, current_stack= %(current_stack)s, summary=%(summary)s WHERE id=%(id)s"
        return connectToMySQL("website_schema").query_db(query,data)

    @classmethod
    def update_instructor(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password= %(password)s, birthday=%(birthday)s, gender=%(gender)s, current_stack= %(current_stack)s, summary=%(summary)s WHERE id=%(id)s"
        return connectToMySQL("website_schema").query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        return connectToMySQL("website_schema").query_db(query)



    @classmethod
    def insert_photo(cls,data):
        query = "UPDATE users SET photo=%(photo)s WHERE id=%(user_id)s"
        return connectToMySQL("website_schema").query_db(query,data)



