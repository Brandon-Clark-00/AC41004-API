from flask import Flask, send_from_directory, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
# from apiHandler import ApiHandler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__, static_url_path='', static_folder='../src/build')
CORS(app)
api = Api(app)

# @app.route("/", defaults={'path':''})
# def serve(path):
#     return send_from_directory(app.static.folder, 'index.html')
#
# api.add_resource(ApiHandler, '/flask/hello')

# db details
username = 'AC41004@theohealth'
password = 'Theohealth!'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server  = 'theohealth.mysql.database.azure.com'
dbname   = '/theohealth'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#USER MODEL
## TODO: fix data type to correct params
class User(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)
    DoB = db.Column(db.Text)
    Email = db.Column(db.Text)
    Address_line_one = db.Column(db.Text)
    Address_line_two = db.Column(db.Text)
    Postcode = db.Column(db.Text)
    isPhysio = db.Column(db.Text)
    physioID = db.Column(db.Text)
    lastOnline = db.Column(db.Text)
    password = db.Column(db.Text)

#testing the db
@app.route('/')
def testdb():
    try:
        users = User.query.all()
        return '<h1>Connected to db :)</h1>'
    except Exception as e:
        print("\nThe error:\n" + str(e) + "\n here we finish")
        return '<h1>Not connected to db :(</h1>'

#to fix JSON error
def user_serializer(user):
    return {
        'userId': user.userID,
        'name': user.Name,
        'dob': user.DoB,
        'email': user.Email,
        'address1': user.Address_line_one,
        'address2': user.Address_line_two,
        'postcode': user.Postcode,
        'isPhysio': user.isPhysio,
        'physioID': user.physioID,
        'lastOnline': user.lastOnline,
        'password': user.password
    }

@app.route('/users')
def getUsers():
    try:
        #astriks unpacks map into array
        return jsonify([*map(user_serializer, User.query.all())])
    except Exception as e:
        print("\nThe error:\n" + str(e) + "\n")
        return 'Error getting users'

if __name__ == '__main__':
    app.run(debug=True)
