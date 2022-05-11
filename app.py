import sqlite3
from flask import Flask,jsonify

app = Flask(__name__)

def connect(query):
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        return res

@app.route('/movie/<title>')
def search_by_title(title):
    query = f""" SELECT title,country,release_year,listed_in AS genre, description
    FROM netflix
    WHERE title == '{title}'
    ORDER BY release_year DESC
    LIMIT 1
    """
    res = connect(query)
    if(len(res) > 0):
        res = res[0]
        resp = {'title':res[0],'country':res[1],'release_year':res[2],'genre':res[3],'description':res[4]}
        return jsonify(resp)
    else:
        return "Такого фильма нету.."

@app.route('/year/<int:year1>-<int:year2>')
def year_search(year1,year2):
    query = f""" SELECT title,release_year
    FROM netflix
    WHERE release_year BETWEEN {year1} AND {year2}
    LIMIT 100
    """
    res = connect(query)
    resp = []
    for i in res:
        resp.append({'title':i[0],'country':i[1]})
    return jsonify(resp)

@app.route('/rating/<rating>')
def rating_search(rating):
    rating = rating.lower()
    ratings = []
    if rating == "children":
        ratings = ['G']
    elif rating == "family":
        ratings = ['G', 'PG', 'PG-13']
    elif rating == "adult":
        ratings = ['R', 'NC-17']
    print(ratings)
    ratings = '\", \"'.join(ratings)
    ratings = f'\"{ratings}\"'

    query = f""" SELECT title,rating,netflix.description
    FROM netflix
    WHERE rating IN ({ratings})
    """
    res = connect(query)
    resp = []
    for i in res:
        resp.append({'title':i[0],'country':i[1]})
    return jsonify(resp)

@app.route('/genre/<genre>')
def genre_search(genre):
    query = f""" SELECT title,netflix.description
    FROM netflix
    WHERE listed_in like '%{genre}%'
    ORDER BY release_year DESC
    LIMIT 10
    """
    res = connect(query)
    resp = []
    for i in res:
        resp.append({'title':i[0],'country':i[1]})
    return jsonify(resp)


def genre_search(act1,act2):
    query = f""" SELECT netflix.cast
    FROM netflix
    WHERE netflix.cast LIKE '%{act1}%' OR netflix.cast LIKE '%{act2}%'
    """
    res = connect(query)
    actors = []
    for cast in res:
        actors.extend(cast[0].split(', '))
    occured = []
    found = []
    for a in actors:
        if(a in occured):
            found.append(a)
        occured.append(a)
    found.remove(act1)
    found.remove(act2)
    found = set(found)


#genre_search('Rose McIver' , 'Ben Lamb')

def type_search(ptype,year,genre):
    query = f""" SELECT title
    FROM netflix
    WHERE netflix.type = '{ptype}' AND release_year = '{year}' AND listed_in LIKE '%{genre}%'
    """
    res = connect(query)
    print(res)

#type_search('TV Show','2016','Dramas')
app.run()