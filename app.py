import os

from flask import Flask, request, render_template, redirect, g
# from sqlite3 import OperationalError
# import sqlite3
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define database location and name
project_dir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///{}".format(os.path.join(project_dir, "urls.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gzwrywxloihsue:0a7d0e6b5952a259c376bd8a0067725a28a27d2421a13fc6792923a7e0e994cb@ec2-50-19-114-27.compute-1.amazonaws.com:5432/demvn1fde4lip7'
# DATABASE = 'urls.db'

db = SQLAlchemy(app)
# host = 'https://spg-redirect.herokuapp.com/'

class Risperdal(db.Model):
    __tablename__ = "Risperdal"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    fileno = db.Column(db.String(10))
    used = db.Column(db.Integer)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

'''
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
'''

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


@app.route('/status')
def status():
    clients = Risperdall.query.all()
    return render_template('status.html', data=all)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    url = 'https://spg-redirect.herokuapp.com/'  # fallback if no URL is found
    try:
        result = db.session.query(Risperdal).filter(Risperdal.fileno == short_url)
        # result = query_db('SELECT * FROM RISP WHERE FILENO=?', [short_url])
        if result is not None and result[2] == 0:
            url = 'https://www.spglawfirm.com/risperdal-message'
            used = int(result[2]) + 1
            fileno = result[1]
            db.session.add(used)
            db.session.add(fileno)
            '''
            with sqlite3.connect('urls.db') as conn:
                        value1 = int(result[2]) + 1
                        value2 = result[1]
                        cursor = conn.cursor()
                        cursor.execute('UPDATE RISP SET USED = ? WHERE FILENO = ?', (value1, value2))
            '''
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
    app.run(debug=True)
