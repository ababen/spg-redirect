from flask import Flask, request, render_template, redirect, g
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Risperdal

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/status')
def status():
    clients = Risperdal.query.all()
    return render_template('status.html', clients=clients)


@app.route('/<fileno>')
def redirect_short_url(fileno):
    # url = 'https://spg-redirect.herokuapp.com/'  # fallback if no URL is found
    url = 'https://www.google.com'
    client = Risperdal.query.filter_by(fileno=fileno).first()
    if client is not None and client.used == 0:
        message = 'Not used'
        counter = client.used + 1
        client.used = counter
        db.session.add(client)
        db.session.commit()
    elif client is None:
        message = 'We are not able to locate your case in our system!'
    else:
        counter = client.used + 1
        client.used = counter
        db.session.add(client)
        db.session.commit()
        message = 'Else: ' + chr(client.used)
    return render_template('error.html', message=message) # return redirect(url)


if __name__ == '__main__':
    app.run()