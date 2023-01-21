"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, flash
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Wishlist
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "our-project"  
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users= User.query.all()
    users= list(
        map(lambda index: index.serialize(), users)
    )
    response_body=jsonify(users)

    return response_body, 200

@app.route('/users', methods=['DELETE'])
def delete_user():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return "Users Deleted"

@app.route("/login", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username, password=password).first()
    access_token = create_access_token(identity=user.id)
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    else:
        return jsonify({ "token": access_token, "user_id": user.id })
    
    return "You're logged in"
    
    

@app.route('/signup', methods=['POST'])
def add_user():
    name= request.json.get('name')
    email = request.json.get('email')
    password= request.json.get('password')
    username=request.json.get('username')
    id=uuid.uuid4()
    user = User.query.filter_by(email=email).first()

    if user:
        return "User already exists"

    new_user= User(username=username, name=name, email=email, password=password, id=id )
    db.session.add(new_user)
    db.session.commit()

    return "welcome"




@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    wishlist = Wishlist.query.all()
    wishlist = list(
        map(lambda index: index.serialize(), wishlist)
    )
    response_body= jsonify(wishlist)
    return response_body, 200

@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
  
    id = request.json.get("id")
    name = request.json.get("name")
    price = request.json.get("price")
    description = request.json.get("description")
    picture = request.json.get("picture")

    existing_item= Wishlist.query.filter_by(item_name=name).first()
    if existing_item:
        return {"msg": "Already added"}

    response= request.json
    item = Wishlist(id =id, item_name= name, item_price= price, item_description= description, picture_url= picture)
    db.session.add(item)
    db.session.commit()
    return jsonify(response) , 200

@app.route('/wishlist/delete', methods=['DELETE'])
def clear_wishlist():
    items =Wishlist.query.all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return "deleted"


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
