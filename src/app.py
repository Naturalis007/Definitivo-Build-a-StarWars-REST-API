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
from models import db, User, People, Planets, Fav_Planets, Fav_People

#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_hello():

    all_users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), all_users))
    
    return jsonify(all_users), 200



@app.route("/people", methods=["GET"])
def get_all_people():

    all_people = People.query.all()
    all_people = list(map(lambda people: people.serialize(), all_people))
    
    return jsonify(all_people), 200

    return jsonify({
        "mensaje": "aca deben estar todos los personajes de sw"
    })


@app.route("/planets", methods=["GET"])
def get_all_planets():

    all_planets = Planets.query.all()
    all_Planets = list(map(lambda planets: planets.serialize(), all_planets))

    return jsonify(all_planets), 200 
    return jsonify({
        "mensaje": "aca deben estar todos los planetas de sw"
    })        
    


@app.route("/users", methods=["GET"])
def get_all_users():

     return jsonify({
        "mensaje": "aca deben estar todos los usuarios"
    })


@app.route("/users/favorites", methods=["GET"])
def get_all_users_fav():

     return jsonify({
        "mensaje": "aca deben estar todos los favoritos de los usuarios"
    })


@app.route("/people/<int:id>", methods=["GET"])
def get_one_people(people_id):
    onepeople = People.query.get(people_id)
    return jsonify(onepeople.serialize())
    return jsonify({
        "mensaje": "esta es la informacion del personaje con id"+str(id)
    })


@app.route("/planets/<int:id>", methods=["GET"])
def get_one_planets(planets_id):
    oneplanets = Planets.query.get(planets_id)
    return jsonify(oneplanets.serialize())
    return jsonify({
        "mensaje": "esta es la informacion del planeta con id"+str(id)
    })

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def post_fav_planet(planet_id):
    one = Planets.query.get(planet_id)
    user = User.query.get(1)
    if(one):
        new_fav = Fav_planets()
        new_fav.email = user.email
        new_fav.planets_id = planets_id
        db.session.add (new_fav)
        db.session.commit()
        return jsonify({
        "mensaje": "el planeta con id" + str(planets_id) + "ha sido agregado"
    })
    else:
        raise APIException("No existe planeta", status_code=404)


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def post_fav_people(people_id):
    one = People.query.get(people_id)
    user = User.query.get(1)
    if(one):
        new_fav = Fav_People()
        new_fav.email = user.email
        new_fav.people_id = people_id
        db.session.add (new_fav)
        db.session.commit()
        return jsonify({
        "mensaje": "el personaje con id" + str(people_id) + "ha sido agregado"
    })
    else:
        raise APIException("No existe personaje", status_code=404)


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_fav_planet(planets_id):
    one = Fav_Planets.query.filter_by(planets_id=planets_id).first()
    user = User.query.get(1)
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "mensaje": "el planeta con id" + str(planets_id) + "ha sido eliminado"
    })
    else:
        raise APIException("No existe planeta", status_code=404)


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_fav_people(people_id):
    one = Fav_People.query.filter_by(people_id=people_id).first()
    user = User.query.get(1)
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "mensaje": "el personaje con id" + str(people_id) + "ha sido eliminado"
    })
    else:
        raise APIException("No existe personaje seleccionado", status_code=404)






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
