from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import deck_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data) -> None:
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.decks=[]

    @classmethod
    def add_user(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, Now(), Now());"
        return connectToMySQL('solo_project_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, data)
        if len(results)<1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, data)
        return cls(results[0])
    

    @classmethod
    def user_decks(cls, data):
        query="SELECT * FROM users left join decks on users.id=decks.user_id where users.id=%(id)s;" 
        results=connectToMySQL('solo_project_schema').query_db(query, data)

        this_user=cls(results[0])
        for row in results:
            one_deck={
                "id": row["decks.id"],
                "name": row["name"],
                "description": row["description"],
                "created_at": row["decks.created_at"],
                "updated_at": row["decks.updated_at"],
                "user_id": row["user_id"]
            }
            deck_instance=deck_model.Deck(one_deck)
            this_user.decks.append(deck_instance)
        return this_user


    @staticmethod
    def validate_user(user):
        is_valid=True
        query="SELECT * FROM users WHERE email=%(email)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, user)

        if not EMAIL_REGEX.match(user["email"]):
            flash("Email is not valid")
            is_valid=False

        if len(results) >= 1:
            flash("Email is already taken")
            is_valid=False

        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters")
            is_valid=False
        
        if len(user["last_name"]) < 3:
            flash("Last Name must be at least 3 characters")
            is_valid=False
        
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid=False
        
        if user["password"]!=user["confirm_password"]: # takes confirm_password from name="----" on our index.html file
            flash("Passwords do not match")
            is_valid=False

        return is_valid