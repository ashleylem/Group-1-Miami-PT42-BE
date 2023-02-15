from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "User"
    id = db.Column(db.String(130), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    username= db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    profile_picture_path= db.Column(db.String(500), nullable=True)
    picture_filename=db.Column(db.String(500), nullable=True)
    followers=db.Column(db.Integer, nullable=True)
    following=db.Column(db.Integer, nullable=True)
    review_points=db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "profile_pic": self.profile_picture_path,
            "followers": self.followers,
            "following": self.following,
            "points":self.review_points,
            "filename": self.picture_filename

            # do not serialize the password, its a security breach
        }
        
class Wishlist(db.Model):
    __tablename__= "Wishlist" 
    user_id= db.Column(db.String(130), db.ForeignKey(User.id), nullable=False)
    product_id=db.Column(db.Integer, primary_key=True, nullable=False)
    item_name= db.Column(db.String(500), nullable=False)
    item_price= db.Column(db.Integer, nullable=False)
    item_description=db.Column(db.String(500), nullable=False)
    picture_url= db.Column(db.String(500), nullable=False)

    
    def __repr__(self):
        return "<Wishlist(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "userId":self.user_id,
            "product_id": self.product_id,
            "name": self.item_name,
            "price": self.item_price,
            "description": self.item_description,
            "picture": self.picture_url
        }

class VideoUploads(db.Model):
    __tablename__= "VideoUploads" 
    user_id= db.Column(db.String(130),db.ForeignKey(User.id),  nullable=False)
    product_id=db.Column(db.Integer, nullable=False,)
    video_id= db.Column(db.String(130), primary_key=True, nullable=False)
    video_name= db.Column(db.String(500), nullable=False)
    video_description=db.Column(db.String(500), nullable=False)
    video_path= db.Column(db.String(500), nullable=False)
    filename=db.Column(db.String(500), nullable=False) 
    picture_url= db.Column(db.String(500), nullable=False)
    
    user = db.relationship("User")

    
    def __repr__(self):
        return "<VideoUploads(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "userId":self.user_id,
            "product_id": self.product_id,
            "video_id": self.video_id,
            "name": self.video_name,
            "description": self.video_description,
            "video_path": self.video_path,
            "filename": self.filename,
            "picture": self.picture_url

        }

class Cart(db.Model):
    __tablename__= "Cart" 
    user_id= db.Column(db.String(130), db.ForeignKey(User.id), nullable=False)
    product_id=db.Column(db.Integer, primary_key=True, nullable=False)
    item_name= db.Column(db.String(500), nullable=False)
    item_price= db.Column(db.Integer, nullable=False)
    item_description=db.Column(db.String(500), nullable=False)
    picture_url= db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return "<Cart(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "userId":self.user_id,
            "product_id": self.product_id,
            "name": self.item_name,
            "price": self.item_price,
            "description": self.item_description,
            "picture": self.picture_url
        }

class Purchased(db.Model):
    __tablename__= "Purchased" 
    user_id= db.Column(db.String(130), db.ForeignKey(User.id), nullable=False)
    product_id=db.Column(db.Integer, primary_key=True, nullable=False)
    item_name= db.Column(db.String(500), nullable=False)
    item_price= db.Column(db.Integer, nullable=False)
    item_description=db.Column(db.String(500), nullable=False)
    picture_url= db.Column(db.String(500), nullable=False)

    
    def __repr__(self):
        return "<Wishlist(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "userId":self.user_id,
            "product_id": self.product_id,
            "name": self.item_name,
            "price": self.item_price,
            "description": self.item_description,
            "picture": self.picture_url
        }

class Products(db.Model):
    __tablename__= "Products" 
    user_id= db.Column(db.String(130), db.ForeignKey(User.id), nullable=False)
    seller_name=db.Column(db.String(130), nullable=True)
    product_id=db.Column(db.Integer, primary_key=True, nullable=False)
    item_name= db.Column(db.String(500), nullable=False)
    item_price= db.Column(db.Integer, nullable=False)
    item_description=db.Column(db.String(500), nullable=False)
    image_path= db.Column(db.String(500), nullable=False)
    filename=db.Column(db.String(500), nullable=False) 
    category_name= db.Column(db.String(500), nullable=False)
    subcategory_name= db.Column(db.String(500), nullable=False)
    product_details=db.Column(db.String(500), nullable=True) 
    sizes=db.Column(db.String(120), nullable=True) 
    shipping_info=db.Column(db.String(500), nullable=True) 

    
    def __repr__(self):
        return "<Products(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "userId":self.user_id,
            "product_id": self.product_id,
            "name": self.item_name,
            "price": self.item_price,
            "description": self.item_description,
            "filename": self.filename,
            "category_name": self.category_name,
            "subcategory_name": self.subcategory_name,
            "sizes":self.sizes,
            "shipping_info": self.shipping_info,
            "product_details": self.product_details,
            "seller_name":self.seller_name

        }
class Sales(db.Model):
    __tablename__= "Sales" 
    sale_id=db.Column(db.Integer, primary_key=True, nullable=False)
    user_id= db.Column(db.String(130), db.ForeignKey(User.id), nullable=False)
    product_id= db.Column(db.Integer, db.ForeignKey(Products.product_id), nullable=False)
    buyer_name=db.Column(db.String(120), nullable=False) 
    buyer_shipping=db.Column(db.String(120), nullable=False)
    fullfilment_status= db.column(db.Boolean) 

    def __repr__(self):
        return "<Sales(id='%s')% self.id>"
    
    def serialize(self):
        return{
            "sale_id":self.sale_id,
            "userId":self.user_id,
            "product_id": self.product_id,
            "buyer_shipping": self.buyer_shipping,
            "fullfilment_status": self.fullfilment_status,
            "buyer_name":self.buyer_name
        }

