from app import db
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

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
