#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import session

from models import *
from search import *

app = Flask(__name__)
app.secret_key = '}0QRVXTN2y6zrlzm5Yr('


@app.route('/', methods=['POST', 'GET'])
def index(results=None):
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        form_data = request.form
        results = search(form_data)
        keyphrase = request.form['keyphrase']
        limit = request.form['limit']
    else:
        keyphrase = ""
        limit = 10
    if results:
        for result in results:
            result['id_string'] = "{:0>6d}".format(result['id'])
    else:
        results = []
    return render_template('index.html', keyphrase=keyphrase, limit=limit, results=results, results_len=len(results))


@app.route('/profile/<int:person_id>', methods=['POST', 'GET'])
def profile(person_id):
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
    if 'username' in session.keys():
        logged_in = True
    else:
        logged_in = False
    profile = {}
    initialize_db()
    try:
        profile = Person.get(Person.id == person_id).__dict__()
        return render_template('profile.html', result=profile, logged_in=logged_in)
    except:
        return render_template('404.html')


@app.route('/edit/<int:person_id>', methods=['POST', 'GET'])
def edit(person_id):
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
    try:
        profile = Person.get(Person.id == person_id).__dict__()
        return render_template('profile.html', result=profile, logged_in=logged_in)
    except:
        return render_template('404.html')


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
    return render_template('insert.html')


@app.route('/create_person', methods=['POST', 'GET'])
def create_person():
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
    initialize_db()
    Person.create(
        name = form_data['name'],
        connection = form_data['connection'],
        employer = form_data['employer'],
        role = form_data['role'],
        contact = form_data['contact'],
        notes = form_data['notes'],
        tags = form_data['tags']
    )
    flash(form_data['name'] + " successfully added to database!")
    return redirect(url_for('insert'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    # login user and return to index if username/password are valid, else return login page
    if request.method == 'POST':
        try:
            user = User.select().where(User.username == request.form['username']).get()
        except:
            flash("That user doesn't look familiar. Either there's a typo, or you be triflin'.")
            return render_template('login.html')
        if user.password == request.form['password']:
            session['username'] = request.form['username']
            flash("Hey there {}! Welcome to the KEC database, The Sexton.".format(session['username']))
            return render_template('index.html')
        else:
            flash("That's not the correct password for that username.")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash("Logged out successfully")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
