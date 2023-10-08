from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Deck:
    def __init__(self, data) -> None:
        self.id=data["id"]
        self.name=data["name"]
        self.description=data["description"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user_id=data["user_id"]
        self.player=[]


    @classmethod  
    def view_decks(cls):
        query="SELECT * FROM decks join users ON decks.user_id=users.id;" 
        results=connectToMySQL('solo_project_schema').query_db(query)

        decks=[]
        for row in results:
            each_deck=cls(row)

            this_player={
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["updated_at"]
            }
            each_deck.player=user_model.User(this_player)
            decks.append(each_deck)
        return decks
    

    @classmethod
    def add_deck(cls, data):
        query="INSERT INTO decks (name, description, created_at, user_id) VALUES (%(name)s, %(description)s, Now(), %(user_id)s);"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    

    @classmethod
    def show_deck(cls, data):
        query="SELECT * FROM decks join users ON decks.user_id=users.id WHERE decks.id=%(id)s;" 
        results=connectToMySQL('solo_project_schema').query_db(query, data)
        print(results)

        the_player={
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["updated_at"]
            }
        our_deck=cls(results[0])
        our_deck.player=user_model.User(the_player)
        print(our_deck.name)
        return our_deck
    

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM decks WHERE decks.id=%(id)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def edit_deck(cls, data):
        query="UPDATE decks SET name=%(name)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    

    @classmethod
    def delete_deck(cls, data):
        query="DELETE FROM decks WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    
    
    
    
    @staticmethod
    def validate_deck(deck):
        is_valid=True
        if len(deck['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid=False
        
        if len(deck["description"]) < 10:
            flash("Description must be at least 10 characters")
            is_valid=False

        return is_valid
    
    @staticmethod
    def validate_update(deck):
        is_valid=True

        if len(deck["name"]) < 2:
            flash("Name must be at least 2 characters")
            is_valid=False
        
        if len(deck["description"]) < 10:
            flash("Description must be at least 10 characters")
            is_valid=False

        return is_valid            
    

    @classmethod
    def add_card(cls, data):
        query="INSERT INTO cards_has_decks (card_name, deck_id, number) VALUES (%(card_name)s, %(deck_id)s, %(number)s);"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    

    @classmethod
    def delete_card(cls, data):
        query="DELETE FROM cards_has_decks WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, data)


    @classmethod
    def get_cards(cls, data):
        query="SELECT * FROM cards_has_decks WHERE deck_id=%(id)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, data)
        return results
    

    @classmethod
    def update_quantity(cls, data):
        query="UPDATE cards_has_decks SET number=%(number)s WHERE id=%(id)s;"
        return connectToMySQL('solo_project_schema').query_db(query, data)
    


    @staticmethod
    def validate_card_quantity(card):
        query="SELECT * FROM cards_has_decks WHERE card_name=%(card_name)s;"
        results=connectToMySQL('solo_project_schema').query_db(query, card)
        print(results)
        is_valid=True

        if len(results) > 0:
            flash("Already included")
            is_valid=False

        return is_valid            
