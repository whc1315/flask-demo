# from datetime import datetime
from flask import (Flask, render_template, abort,
                   jsonify, request, redirect, url_for)

from model import db, save_db


app = Flask(__name__)


@app.route("/")
def welcome():
    # return "Welcome to my Flash Card application!"
    return render_template("welcome.html", cards=db)


@app.route("/card/<int:index>")
def view_card(index):
    try:
        card = db[index]
        return render_template("card.html", card=card, index=index, max_index=len(db)-1)
    except IndexError:
        abort(404)


@app.route('/api/card/')
def api_card_list():
    return jsonify(db)


@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route('/add_card', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('view_card', index=len(db)-1))
    else:
        return render_template("add_card.html")


@app.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except:
        abort(404)

# @app.route("/date")
# def date():
#     return "This page was served at " + str(datetime.now())


# counter = 0


# @app.route("/count_views")
# def count_views():
#     global counter
#     counter += 1
#     return "This page has been viewed " + str(counter) + " times!"
