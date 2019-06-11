from flask import Flask, request, render_template, redirect, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, Session, sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from twilio.rest import Client
from datetime import datetime
import os

app = Flask(__name__)

# Configure Database
database = os.environ.get('DATABASE_URL')
engine = create_engine("mysql://pqk33wgherx3o3nd:li1jefgw2dk0rqd9@wp433upk59nnhpoh.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/snjg4buvgg8td7qa")
Session = sessionmaker(bind=engine)
session = Session()

# Configure Twilio
DEFAULT_NUMBER = '+15165481903'
app.config['TWILIO_ACCOUNT_SID'] = os.environ.get('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')

Base = declarative_base()

class Risperdal(Base):
    __tablename__ = "Risperdal"
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    fileno = Column(String(10))
    used = Column(Integer)
    phone = Column(String, nullable=True)

    def __init__(self, email, fileno, used):
        self.email = email
        self.fileno = fileno
        self.used = used

    def __repr__(self):
        return '<E-mail %r>' % self.email


class Risperdal_Messages(Base):
    __tablename__ = "Risperdal_Messages"
    id = Column(Integer, primary_key=True)
    fk_risperdal = Column(Integer, ForeignKey('Risperdal.id'))
    to = Column(String(12), nullable=True)
    timestamp_ = Column(DateTime, nullable=True, default=datetime.utcnow)
    message = Column(String(360), nullable=True)
    risperdal = relationship("Risperdal", back_populates = "Risperdal")

    def __init__(self, fk_risperdal, to, message):
        self.fk_risperdal = fk_risperdal
        self.to = to
        self.timestamp_ = timestamp_
        self.message = message


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


@app.route('/sms_send')
def home():
    clients = session.query(Risperdal).all()
    client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

    message = client.messages \
        .create(
            body="Important message from your lawyer! Click:https://www.google.com",
            from_='+15165481903',
            to='+15166470658'
        )

    print(message.sid)

    return render_template('sms.html', clients=clients)


@app.route('/status')
def status():
    clients = session.query(Risperdal).all()
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
        message = 'We are not able to locate your case in our system! Please contact our office: (516) 741-5600'
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
