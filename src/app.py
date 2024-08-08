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
from models import db, Teachers, Students, Cohorts, Subjects
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/teachers', methods=['GET'])
#Get ALL teachers
def get_all_teachers():
    if request.method == 'GET':
        return Teachers.query.all()

@app.route('/teacher/<int:id>', methods=['GET', 'DELETE', 'POST'])
#Get ONE teacher, route singular since getting ONE teacher
def get_one_teacher():
    if request.method == 'GET':
        return Teachers.query.filter_by(id)
    elif request.method == 'DELETE':
        Teachers.query.filter_by(id).delete()
        db.session.commit()
        return 
    elif request.method == 'POST':
        email =  request.form["email"] #this assumes that the request I'm getting has an email. 
        name = request.form['name']
        experience = request.form['experience']
        subjects = request.form['subjects']
        is_active = request.form['is_active']
        add = Teachers(id, email, name, experience, subjects, is_active )
        db.session.add(add)
        db.session.commit()
        
        return jsonify(add), 200

#@app.route('/students', methods=['GET'])
#get ALL students

#@app.route('/student/<int:id >', methods=['GET', 'DELETE', 'POST'])
#get ONE student, route singular since getting ONE student

#@app.route('/subjects', methods=['GET'])
#get subjects

#@app.route('/cohorts', methods=['GET'])
#get cohorts





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
