from app import db

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
