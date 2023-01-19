from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "User"
    id = db.Column(db.String(130), db.ForeignKey("Wishlist.user_id"), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    username= db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Wishlist(db.Model):
    __tablename__= "Wishlist"
    user_id= db.Column(db.String(130,))
    id =db.Column(db.Integer, primary_key=True)
    item_name= db.Column(db.String(500), nullable=False)
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

    