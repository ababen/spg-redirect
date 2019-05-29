from flask import Flask, request, render_template, redirect, g
from sqlite3 import OperationalError
import sqlite3

# Assuming urls.db is in your app root folder
app = Flask(__name__)
DATABASE = 'urls.db'
# host = 'https://spg-redirect.herokuapp.com/'


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


def update_count(result):
    with sqlite3.connect('urls.db') as conn:
                value1 = int(result[2]) + 1
                value2 = result[1]
                cursor = conn.cursor()
                cursor.execute('UPDATE RISP SET USED = ? WHERE FILENO = ?', (value1, value2))
                return cursor


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    url = 'https://spg-redirect.herokuapp.com/'  # fallback if no URL is found
    try:
        result = query_db('SELECT * FROM RISP WHERE FILENO=?', [short_url])
        if result is not None and result[2] == 0:
            url = 'https://www.spglawfirm.com/risperdal-message'
            with sqlite3.connect('urls.db') as conn:
                        value1 = int(result[2]) + 1
                        value2 = result[1]
                        cursor = conn.cursor()
                        cursor.execute('UPDATE RISP SET USED = ? WHERE FILENO = ?', (value1, value2))
        elif result is None:
            message = 'We are not able to locate your case'
            return render_template('error.html', message=message)
        else:
            update_count(result)
            url = 'https://www.spglawfirm.com/risperdal-message-thank-you/'
            return redirect(url)
    except Exception as e:
        print(e)
        message = 'There is some kind of error!'
        return render_template('error.html', message=message)
    return redirect(url)


if __name__ == '__main__':
    app.run()