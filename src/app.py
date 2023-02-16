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
from models import db, User, Wishlist,VideoUploads, Purchased, Cart, Products, Sales
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid
from werkzeug.utils import secure_filename

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
UPLOADS_FOLDER=  os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER

PRODUCTS_FOLDER=  os.path.abspath(os.path.join(os.path.dirname(__file__), 'Products'))
app.config['PRODUCTS_FOLDER']= PRODUCTS_FOLDER

PROFILEPICS_FOLDER=  os.path.abspath(os.path.join(os.path.dirname(__file__), 'ProfilePics'))
app.config['PROFILEPICS_FOLDER']= PROFILEPICS_FOLDER


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

@app.route('/<user_id>', methods=['GET'])
def get_user_info(user_id):
    user= User.query.filter_by(id=user_id)
    user= list(
        map(lambda index: index.serialize(), user)
    )
    response_body= jsonify(user)
    return response_body, 200

@app.route('/users', methods=['DELETE'])
def delete_user():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return "Users Deleted"

@app.route('/<user_id>/picture', methods=['POST'])
def add_profile_pic(user_id):
    user= User.query.get(user_id)

    if 'file' not in request.files:
        flash('No file part in request')
        
    file =request.files['file']
    
    if file and file_valid(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['PROFILEPICS_FOLDER'], filename))
        user.profile_picture_path= os.path.abspath(PROFILEPICS_FOLDER)
        user.picture_filename= filename
        db.session.commit()
    return "successfully added"

@app.route('/profile/picture/<path:path>')
def send_profile_image(path):
    return send_from_directory(app.config['PROFILEPICS_FOLDER'], path)

@app.route('/profile/picture/replace/<user_id>', methods=["POST"])
def replace_profile_pic(user_id):
    user= User.query.get(user_id)
    filename=user.picture_filename
    user.profile_picture_path= None
    user.picture_filename= None
    os.remove(os.path.join(app.config['PROFILEPICS_FOLDER'], filename))

    if 'file' not in request.files:
        flash('No file part in request')
        
    file =request.files['file']
    
    if file and file_valid(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['PROFILEPICS_FOLDER'], filename))
        user.profile_picture_path= os.path.abspath(PROFILEPICS_FOLDER)
        user.picture_filename= filename
        db.session.commit()
    return "successfully replaced"


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

@app.route('/videos/<path:path>')
def send_video(path):
    return send_from_directory(app.config['UPLOADS_FOLDER'], path)


@app.route('/videos/delete', methods=['DELETE'])
def delete_video():
    videos=VideoUploads.query.all()
    for video in videos:
        os.remove(os.path.join(app.config['UPLOADS_FOLDER'], video.filename))
        db.session.delete(video)
        
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
    filename = request.json.get("picture")

    existing_item= Cart.query.filter_by(item_name=name).first()
    if existing_item:
        return {"msg": "Already added"}

    response= request.json
    item = Cart(user_id= userID, product_id =id, item_name= name, item_price= price, item_description= description, picture_url= filename)
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

@app.route('/sales', methods=['POST'])
def user_sales():
    user_id=request.form.get("user_id")
    product_id= request.form.get("product_id")
    buyer_name=request.form.get("buyer_name")
    buyer_shipping=request.form.get("buyer_shipping")
    sale_id=uuid.uuid4()
    fullfilment_status=request.form.get("fullfilment_status")

    newSale= Sales(userId=user_id, product_id=product_id, buyer_name=buyer_name, buyer_shipping=buyer_shipping, sale_id=sale_id, fullfilment_status=fullfilment_status)
    db.session.add(newSale)
    db.session.commit()

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
@app.route('/purchases/delete', methods=['DELETE'])
def clear_purchases():
    items =Purchased.query.all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return "deleted"

@app.route('/products', methods=['POST'])
def add_products():
    user_id=request.form.get('userId')
    product_id=uuid.uuid4()
    name=request.form.get('name')
    description=request.form.get('description')
    price=request.form.get('price')
    category_name=request.form.get('category_name')
    subcategory_name=request.form.get('subcategory_name')
    shipping_info=request.form.get('shipping')
    sizes=request.form.get('sizes')
    product_details=request.form.get('product_details')

    if 'file' not in request.files:
        flash('No file part in request')
        
    images =request.files.getlist('file')
    
    image_paths = []
    image_filenames = []

    for image in images:
        if file_valid(image.filename):
            filename=secure_filename(image.filename)
            image.save(os.path.join(app.config['PRODUCTS_FOLDER'], filename))
            path = os.path.join(app.config['PRODUCTS_FOLDER'], filename)
            image_paths.append(path)
            image_filenames.append(filename)

    image_path_str = ','.join(image_paths)
    image_filenames_str= ','.join(image_filenames)
    newProduct= Products(user_id=user_id, item_price=price, item_name=name, item_description=description, image_path=image_path_str, filename=image_filenames_str, subcategory_name=subcategory_name, category_name=category_name, sizes=sizes, product_details=product_details, shipping_info=shipping_info )

    db.session.add(newProduct)
    db.session.commit() 
   
    return "successfully added"

@app.route('/products', methods=['GET'])
def get_products():
    products= Products.query.all()
    productsInfo= list(
        map(lambda item: item.serialize(), products)
    )

    response_body=jsonify(productsInfo)
    return response_body, 200 
    
@app.route('/<user_id>/<product_id>/product/edit', methods=['POST'])
def edit_product(user_id, product_id):
    product= Products.query.filter_by(product_id=product_id).first()
    attribute_map = {
        "item_name": "item_name",
        "item_price": "item_price",
        "item_description":"item_description",
        "category_name": "category_name",
        "subcategory_name": "subcategory_name",
        "sizes":"sizes",
        "shipping_info": "shipping_info",
        "product_details": "product_details",
        "seller_name":"seller_name"
}
    form_data = request.form
    item_key = list(form_data.keys())[0]
    if item_key in attribute_map:
        setattr(product, attribute_map[item_key], form_data[item_key])
        db.session.commit()
        return 'Successfully changed'
 


@app.route('/products/<user_id>', methods=['GET'])
def get_user_products(user_id):
    products= Products.query.filter_by(user_id=user_id).all()
    product_data = []
    for product in products:
        product_data.append({
            'id': product.product_id,
            'name': product.item_name,
            'description': product.item_description,
            'price': product.item_price,
            'image_paths': product.image_path.split(','),
            'category': product.category_name,
            'subcategory':product.subcategory_name,
            'sizes':product.sizes,
            'details':product.product_details,
            'shipping':product.shipping_info
        })
    return jsonify({'products': product_data})
    
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('/workspace/Group-1-Miami-PT42-BE/', path)

@app.route('/product/images/<filename>', methods=["GET"])
def send_product_image(filename):
    return send_from_directory(app.config['PRODUCTS_FOLDER'], filename)

@app.route('/products/<int:product_id>', methods=["GET"])
def get_product_info(product_id):
    product= Products.query.filter_by(product_id=product_id).first()
    if product:
        serialized_product = product.serialize()
        return jsonify(serialized_product)
    else:
        return jsonify({"error": "Product not found"})


@app.route('/products/delete', methods=['DELETE'])
def delete_images():
    products=Products.query.all()
    for product in products:
        db.session.delete(product)
        for image in  product.filename.split(','):
            os.remove(os.path.join(app.config['PRODUCTS_FOLDER'], image))
    db.session.commit()
    return "deleted"

@app.route('/accessories', methods=["GET"])
def get_accessories():
    accessories = Products.query.filter_by(category_name="Accessories").all()
    accessories= list(
        map(lambda item: item.serialize(), accessories)
    )
    response_body=jsonify(accessories)
    return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

