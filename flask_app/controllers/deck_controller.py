from flask import Flask, render_template, request, session, redirect, flash
import requests
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.deck_model import Deck



@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/logout')
    
    data={
        "id": session["user_id"]
    }
    decks=Deck.view_decks()
    user=User.get_by_id(data)
    return render_template("dashboard.html", user=user, decks=decks)



@app.route('/decks/new', methods=['GET', 'POST']) 
def new_deck():
    if "user_id" not in session:
        return redirect('/logout') 
    
    if request.method=='GET':
        return render_template("new_deck.html")
    
    else:
        if not Deck.validate_deck(request.form):
            return render_template("new_deck.html")
        
        data={
            "name": request.form["name"],
            "description": request.form["description"],
            "user_id": session["user_id"]
            }
        Deck.add_deck(data)
        print(data)
    return redirect('/dashboard')
    
    
@app.route('/decks/<int:id>')
def view_deck(id):
    if "user_id" not in session: 
        return redirect('/logout') 
    
    data={
        "id": id
    }
    data2={
        "id": session["user_id"]
    }

    deck=Deck.show_deck(data)
    user=User.get_by_id(data2)
    list=Deck.get_cards(data)
    return render_template("show_deck.html", deck=deck, user=user, list=list)


@app.route('/decks/edit/<int:id>')
def edit_deck(id):
    if "user_id" not in session:
        return redirect('/logout')
    
    data={
        "id": id
    }
    
    deck=Deck.get_one(data)
    options=[]
    search="High Ground"
    url="https://api.magicthegathering.io/v1/cards"
    response=requests.get(url)
    api_data=response.json()
    print("this is a response", response)
    # print("api_data", api_data)
    cards=api_data["cards"]
    for i in cards:
        # if search==i["name"]:
        options.append(i["name"])

    list=Deck.get_cards(data)
    
    data2={
        "id": session["user_id"]
    }
    user=User.get_by_id(data2)

    return render_template("edit_deck.html", deck=deck, options=options, list=list, user=user)


@app.route('/decks/update/<int:id>', methods=['POST'])
def update_deck(id):
    if "user_id" not in session:
        return redirect('/logout')

    else:
        if not Deck.validate_update(request.form):
            print("validation failed")
            # return render_template("edit_deck.html")
            return redirect(f'/decks/edit/{id}')

    data={
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"]
    }
    
    if request.form["card_name"]!="":
        if not Deck.validate_card_quantity(request.form):
            return redirect(f'/decks/edit/{id}')
        if request.form["number"]!="":
            data2={
                "id": id,
                "card_name": request.form["card_name"],
                "deck_id": id,
                "number": request.form["number"]
            }
            Deck.add_card(data2)
    Deck.edit_deck(data)    
    return redirect('/dashboard')


@app.route('/decks/increase/<int:id>/<int:deck_id>/<int:quantity>')
def add_card_quantity(id, deck_id, quantity):
    if "user_id" not in session: 
        return redirect('/logout') 
    
    data={
        "id": id,
        "number": quantity+1
    }
    Deck.update_quantity(data)
    return redirect(f'/decks/edit/{deck_id}')


@app.route('/decks/decrease/<int:id>/<int:deck_id>/<int:quantity>')
def decrease_card_quantity(id, deck_id, quantity):
    if "user_id" not in session: 
        return redirect('/logout') 
    
    data={
        "id": id,
        "number": quantity-1
    }
    Deck.update_quantity(data)
    return redirect(f'/decks/edit/{deck_id}')


@app.route('/decks/delete/<int:id>/<deck_id>')
def delete_card(id, deck_id):
    if "user_id" not in session: 
        return redirect('/logout')
    
    data={
        "id": id
    }
    Deck.delete_card(data)
    return redirect(f'/decks/edit/{deck_id}')


@app.route('/decks/delete/<int:id>')
def delete_deck(id):
    if "user_id" not in session: 
        return redirect('/logout')
    
    data={
        "id": id
    }
    Deck.delete_deck(data)
    return redirect('/dashboard')