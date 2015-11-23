from operator import itemgetter

from flask import request
from flask import flash

from flask import session
from models import *

def create_blob(this_dict):
    blob = ""
    for key in this_dict:
        if ((key != 'id') and (key != 'score')):
            blob += ' ' + this_dict[key] + ' '
        elif key == 'id':
            blob += ' ' + str(this_dict[key]) + ' '
    return blob.lower()

def search_ranking(results, keywords, limit):
    for result in results:
        blob = create_blob(result)
        for keyword in keywords:
            if keyword.lower() in blob:
                result['score'] +=  20

            if keyword.lower() in result['name'].lower():
                result['score'] += 10
            if keyword.lower() in result['employer'].lower():
                result['score'] += 5
            if keyword.lower() in result['role'].lower():
                result['score'] += 5
            if keyword.lower() == str(result['id']):
                result['score'] += 20

            result['score'] += 2 * blob.count(' ' + keyword.lower() + ' ')

            result['score'] += blob.count(keyword)

    results = sorted(results, key=itemgetter('score'), reverse=True)
    if len(results) > int(limit):
        results = results[0:int(limit)]
    return results

def search(form_data):
    if 'username' not in session.keys():
        flash("You need to be logged in to access this page.")
        return redirect(url_for('login'))
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
    results = search_ranking(results=results, keywords=keywords, limit=form_data['limit'])
    if len(results) == 0:
        flash("Sorry, no results turned up for \"{}\"".format(keyphrase))
    elif len(results) == 1:
        flash("Returned 1 result for \"{}\"".format(keyphrase))
    else:
        flash("Returned {} results for \"{}\"".format(len(results), keyphrase))
    return results
