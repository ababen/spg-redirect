from flask import Flask, request, render_template, redirect, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import os

app = Flask(__name__)

engine = create_engine('mysql://pqk33wgherx3o3nd:li1jefgw2dk0rqd9@wp433upk59nnhpoh.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/snjg4buvgg8td7qa')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Risperdal(Base):
    __tablename__ = "Risperdal"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    fileno = Column(String(10))
    used = Column(Integer)

    def __init__(self, email, fileno, used):
        self.email = email
        self.fileno = fileno
        self.used = used

    def __repr__(self):
        return '<E-mail %r>' % self.email

Base.metadata.create_all(engine)

c1 = Risperdal(email='michael@jackson.com',
                fileno='12345',
                used='0')

c2 = Risperdal(email='matt@damon.com',
                fileno='54321',
                used='0')
if not session.query(Risperdal).filter(Risperdal.fileno == '12345').first():
    session.add(c1)
    session.add(c2)
    session.commit()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/status')
def status():
    clients = session.query.all()
    return render_template('status.html', clients=clients)


@app.route('/<fileno>')
def redirect_short_url(fileno):
    url = 'https://spg-redirect.herokuapp.com/'  # fallback if no URL is found
    client = session.query(Risperdal).filter(Risperdal.fileno==fileno).first()
    if client is not None and client.used == 0:
        message = 'Not used'
        counter = client.used + 1
        client.used = counter
        session.add(client)
        session.commit()
        url = 'https://www.spglawfirm.com/risperdal-message'
        return redirect(url)
    elif client is None:
        message = 'We are not able to locate your case in our system!'
        return render_template('error.html', message=message)
    else:
        counter = client.used + 1
        client.used = counter
        session.add(client)
        session.commit()
        url = 'https://www.spglawfirm.com/risperdal-message-thank-you'
    return redirect(url)


if __name__ == '__main__':
    app.run()