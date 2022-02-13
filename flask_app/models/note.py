from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Note:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.content = data["content"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def delete_note(cls,data):
        query = "DELETE FROM notes WHERE id = %(id)s"
        return connectToMySQL("website_schema").query_db(query,data)

    @classmethod
    def insert_note(cls,data):
        query = "INSERT INTO notes (user_id, title, content) VALUES ( %(user_id)s, %(title)s, %(content)s)"
        return connectToMySQL("website_schema").query_db(query,data)

    @classmethod
    def get_notes(cls):
        query = "SELECT * FROM notes"
        return connectToMySQL("website_schema").query_db(query)


    @classmethod
    def get_note(cls,data):
        query = "SELECT * FROM notes WHERE id = %(id)s"
        note = connectToMySQL("website_schema").query_db(query,data)
        return cls(note[0])

    @classmethod
    def update_note(cls,data):
        query = "UPDATE notes SET title=%(title)s, content=%(content)s  WHERE id=%(id)s"
        return connectToMySQL("website_schema").query_db(query,data)







    @staticmethod
    def validate_recipe(recipe):        
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Name of the recipe must be longer than 3 characters.")
            is_valid = False
        if "under_30" not in recipe:
            flash("You have to choose yes or no.")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description must be longer than 3 characters.")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Your instrustions must be longer than 3 characters")
            is_valid = False
        if len(recipe["created_at"]) < 1:
            flash("You need to choose a date.")
            is_valid = False
        return is_valid

