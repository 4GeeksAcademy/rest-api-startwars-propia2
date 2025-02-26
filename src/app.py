"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favoritos
#from models import Person
CURRENT_USER_ID=5

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Person.query.all()
    result = [person.serialize() for person in people]
    return jsonify({"result": result})

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Person.query.get(people_id)
    if  Person.query.get(people_id) is None:
        return jsonify({"msg" : "person doesnt exist"})
    return jsonify(person.serialize())

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    if result is None:
        return jsonify({"msg" : "no planets saved"})
    
    return jsonify({"result" : result})

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg" : "planet doesnt exist"})
    return jsonify(planet.serialize())

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify({"result" : result})

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favoritos = Favoritos.query.filter_by(user_id=CURRENT_USER_ID).first()
    if favoritos is None:
        return jsonify({"msg" : "no favorites added"})
    return jsonify(favoritos.serialize())
    
@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_active = request.json.get("is_active", True)

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg" : "user already exists"})
    
    new_user = User(email=email, password=password, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg" : "user created succesfully"})

@app.route('/addplanet', methods=['POST'])
def add_planet():
    name = request.json.get("name", None)
    temp = request.json.get("temp", None)
    size = request.json.get("size", None)

    if Planet.query.filter_by(name=name).first() is not None:
        return jsonify({"msg" : "planet already exists"})
    
    new_planet = Planet(name=name, temp=temp, size=size)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg" : "planet created succesfully"})

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    existe = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if existe is None:
        new_favorite_planet = Favoritos(user_id=CURRENT_USER_ID,planet_id=planet_id)
        db.session.add(new_favorite_planet)
        db.session.commit()

        return jsonify({"msg" : "planet added to favorites"})
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    exist = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if exist:
        db.session.delete(exist)
        db.session.commit()

        return jsonify({"msg" : "planet removed succesfully"})

 # AQUI EMPIEZA EL SEGUNDO CODIGO:
    
@app.route('/user1', methods=['GET'])
def get_my_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify({ "result" : result})

@app.route('/planet1/<int:planet_id>', methods=['GET'])
def get_my_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg" : "planet doesnt exist"}), 404
    return jsonify(planet.serialize())

@app.route('/user1/favoritos', methods=['GET'])
def get_my_favorites():
    favoritos = Favoritos.query.filter_by(user_id=CURRENT_USER_ID).first()
    return jsonify(favoritos.serialize())

@app.route('/registro', methods=['POST'])
def registro():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_active = request.json.get("is_active", True)

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg" : "user already exists"}), 400
    
    new_user = User(email=email, password=password, is_active= is_active)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg" : "user created succesfully"})

@app.route('/añadir_planeta/favoritos/<int:planet_id>', methods=['POST'])
def añadir_planeta(planet_id):
    existe = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first()
    if existe is None:
        new_fucking_planet = Favoritos(user_id=CURRENT_USER_ID, planet_id=planet_id)
        db.session.add(new_fucking_planet)
        db.session.commit()
        return jsonify({"msg" : "planet added to favorites"})













    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
