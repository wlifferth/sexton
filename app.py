#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import flash

from models import *
from search_ranking import *

app = Flask(__name__)
app.secret_key = '}0QRVXTN2y6zrlzm5Yr('


@app.route('/', methods=['POST', 'GET'])
def index(results=None):
    if request.method == 'POST':
        form_data = request.form
        results = search(form_data)
    try:
        keyphrase = request.form['keyphrase']
    except:
        keyphrase = ""
    try:
        limit = request.form['limit']
    except:
        limit = 10
    if results:
        for result in results:
            result['id_string'] = "{:0>6d}".format(result['id'])
    else:
        results = []
        return render_template('index.html', keyphrase=keyphrase, limit=limit, results=None, results_len=None)
    return render_template('index.html', keyphrase=keyphrase, limit=limit, results=results, results_len=len(results))



@app.route('/profile/<int:person_id>', methods=['POST', 'GET'])
def profile(person_id):
    profile = {}
    initialize_db()
    try:
        profile = Person.get(Person.id == person_id).__dict__()
        return render_template('profile.html', result=profile)
    except:
        return render_template('404.html')

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    return render_template('insert.html')

@app.route('/search', methods=['POST', 'GET'])
def search(form_data):
    initialize_db()
    keyphrase = request.form['keyphrase']
    keywords = keyphrase.split()
    results = []
    for keyword in keywords:
        try:
            id_int = int(keyword)
        except:
            id_int = 0
        for person in Person.select().where(
            (
                Person.name
                .concat(Person.connection)
                .concat(Person.employer)
                .concat(Person.role)
                .concat(Person.contact)
                .concat(Person.notes)
                .concat(Person.tags)
            ).contains(keyword) |
            (Person.id == id_int)
        ):
            if person.__dict__() not in results:
                results.append(person.__dict__())
    if len(results) == 0:
        flash("Sorry, no results turned up for \"{}\"".format(keyphrase))
    elif len(results) == 1:
        flash("Returned 1 result for \"{}\"".format(keyphrase))
    else:
        flash("Returned {} results for \"{}\"".format(len(results), keyphrase))
    results = search_ranking(results=results, keywords=keywords, limit=form_data['limit'])
    return results

@app.route('/create_person', methods=['POST', 'GET'])
def create_person():
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
    flash(form_data['name'] + ' successfully added to database!')
    return redirect(url_for('insert'))


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
