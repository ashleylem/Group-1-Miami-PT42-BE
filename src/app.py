"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, flash, send_from_directory, send_file
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
from utils import APIException, generate_sitemap, file_valid
from admin import setup_admin
from models import db, User, Wishlist,VideoUploads, Purchased, Cart
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid
from werkzeug.utils import secure_filename

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
UPLOADS_FOLDER= 'src/Uploads'
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


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
        return jsonify({ "token": access_token, "userId": user.id })
    
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
@jwt_required()
def add_to_wishlist():
    userID= request.json.get('userId')
    id = request.json.get("id")
    name = request.json.get("name")
    price = request.json.get("price")
    description = request.json.get("description")
    picture = request.json.get("picture")

    existing_item= Wishlist.query.filter_by(item_name=name).first()
    if existing_item:
        return {"msg": "Already added"}

    response= request.json
    item = Wishlist(user_id= userID, product_id =id, item_name= name, item_price= price, item_description= description, picture_url= picture)
    db.session.add(item)
    db.session.commit()
    return jsonify(response) , 200

@app.route('/wishlist/<userId>', methods=['GET'])
@jwt_required()
def get_user_wishlist(userId):
    items= Wishlist.query.filter_by(user_id=userId).all()
    items= list(
        map(lambda index: index.serialize(), items)
    )
    return jsonify(items)

@app.route('/wishlist/<user_id>/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_item(user_id, product_id):
    item= Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    db.session.delete(item)
    db.session.commit()
    return {"msg": "item deleted"}


@app.route('/wishlist/delete', methods=['DELETE'])
def clear_wishlist():
    items =Wishlist.query.all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return "deleted"
@app.route('/uploads/videos', methods=['GET'])
def get_videos():
    videos= VideoUploads.query.all()
    videos= list(
        map(lambda index: index.serialize(), videos)
    )
    response_body=jsonify(videos)

    return response_body, 200
    
@app.route('/uploads/videos', methods=['POST'])
def upload_video():
    user_id=request.form.get('userId')
    product_id=request.form.get('product_id')
    video_id=uuid.uuid4() 
    name=request.form.get('name')
    description=request.form.get('description')
    filename=request.files.get('filename')
    picture=request.form.get('picture')
    

    if 'file' not in request.files:
        flash('No file part in request')
        
    file =request.files['file']
    
    if file and file_valid(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        newUpload= VideoUploads(user_id=user_id, product_id=product_id, video_id=video_id, video_name=name, video_description=description, video_path=os.path.abspath(UPLOADS_FOLDER), filename=filename, picture_url=picture )
        db.session.add(newUpload)
        db.session.commit()
    return "successfully added"

@app.route('/uploads/videosInfo/<user_id>', methods=['GET'])
def get_user_videosInfo(user_id):
    videos= VideoUploads.query.filter_by(user_id=user_id).all()
    videosInfo= list(
        map(lambda item: item.serialize(), videos)
    )
    # for video in videos:
    #     return send_from_directory(video.video_path, video.filename, mimetype='video/mp4')

    response_body=jsonify(videosInfo)
    return response_body, 200 

@app.route('/uploads/videos/<video_id>', methods=['GET'])
def get_user_videos(video_id):
    video= VideoUploads.query.filter_by(video_id=video_id).first()
    videoI= video.serialize()
    filename= videoI.get('filename')
    path=videoI.get('video_path')

    return send_from_directory(path, filename, mimetype='video/mp4'), 200

    

@app.route('/videos/delete', methods=['DELETE'])
def delete_video():
    videos=VideoUploads.query.all()
    for video in videos:
        db.session.delete(video)
        os.remove(os.path.join(app.config['UPLOADS_FOLDER'], video.filename))
    db.session.commit()
    return "deleted"


@app.route('/Cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    userID= request.json.get('userId')
    id = request.json.get("id")
    name = request.json.get("name")
    price = request.json.get("price")
    description = request.json.get("description")
    picture = request.json.get("picture")

    existing_item= Cart.query.filter_by(item_name=name).first()
    if existing_item:
        return {"msg": "Already added"}

    response= request.json
    item = Cart(user_id= userID, product_id =id, item_name= name, item_price= price, item_description= description, picture_url= picture)
    db.session.add(item)
    db.session.commit()
    return jsonify(response) , 200

@app.route('/Cart/<userId>', methods=['GET'])
@jwt_required()
def get_user_cart(userId):
    items= Cart.query.filter_by(user_id=userId).all()
    items= list(
        map(lambda index: index.serialize(), items)
    )
    return jsonify(items)

@app.route('/Cart/<user_id>/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(user_id, product_id):
    item= Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    db.session.delete(item)
    db.session.commit()
    return {"msg": "item deleted"}


@app.route('/Cart/<user_id>/delete', methods=['DELETE'])
@jwt_required()
def clear_user_cart(user_id):
    items =Cart.query.filter_by(user_id=user_id).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return "deleted"


@app.route('/purchased', methods=['POST'])
@jwt_required()
def purchased_items():
    response= request.json
    userID= request.json.get('userId')
    id = request.json.get("product_id")
    name = request.json.get("name")
    price = request.json.get("price")
    description = request.json.get("description")
    picture = request.json.get("picture")
    
    newitem = Purchased(user_id= userID, product_id =id, item_name= name, item_price= price, item_description= description, picture_url= picture)
    db.session.add(newitem)
    db.session.commit()


    return response , 200

@app.route('/purchased', methods=['GET'])
def get_purchases():
    purchase = Purchased.query.all()
    purchase = list(
        map(lambda index: index.serialize(), purchase)
    )
    response_body= jsonify(purchase)
    return response_body, 200
        

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

