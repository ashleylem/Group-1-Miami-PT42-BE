from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Wishlist(db.Model):
    __tablename__= "Wishlist"
    id =db.Column(db.Integer, primary_key=True)
    item_name= db.Column(db.String(120), nullable=False)
    item_price= db.Column(db.Integer, nullable=False)
    item_description=db.Column(db.String(500), nullable=False)
    picture_url= db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return "<Wishlist(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.item_name,
            "price": self.item_price,
            "description": self.item_description,
            "picture": self.picture_url
        }

    