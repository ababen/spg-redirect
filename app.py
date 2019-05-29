from flask import Flask, request, render_template, redirect, g
from sqlite3 import OperationalError
import sqlite3

from math import floor
import string
try:
    from urllib.parse import urlparse  # Python 3
    str_encode = str.encode
except ImportError:
    from urlparse import urlparse  # Python 2
    str_encode = str
try:
    from string import ascii_lowercase
    from string import ascii_uppercase
except ImportError:
    from string import lowercase as ascii_lowercase
    from string import uppercase as ascii_uppercase
import base64


# Assuming urls.db is in your app root folder
app = Flask(__name__)
host = 'https://spg-redirect.herokuapp.com/'
DATABASE = 'urls.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    url = host  # fallback if no URL is found
    try:
        result = query_db('SELECT * FROM RISP WHERE FILENO=?', [short_url])
        if result is not None and result[2] < 1:
            url = 'https://www.spglawfirm.com/risperdal-message'
            with sqlite3.connect('urls.db') as conn:
                        value1 = int(result[2]) + 1
                        value2 = result[1]
                        cursor = conn.cursor()
                        cursor.execute('UPDATE RISP SET USED = ? WHERE FILENO = ?', (value1, value2))
        elif result is None:
            message = 'We are not able to locate your case'
            url = 'error.html'
            return redirect(url, Response=message)
        else:
            print('This URL has already been used.')
            url = 'https://www.spglawfirm.com/risperdal-message-thank-you/'
            return redirect(url)
    except Exception as e:
        print(e)
    return redirect(url)


if __name__ == '__main__':
    # This code checks whether database table is created or not
    # table_check()
    # app.run(debug=True)
    app.run()
