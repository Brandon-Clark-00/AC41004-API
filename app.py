from flask import Flask, send_from_directory, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
# from apiHandler import ApiHandler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import ast

app = Flask(__name__)
CORS(app)
api = Api(app)

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

#SENSOR MODEL
## TODO: fix data type to correct params
class Sensor(db.Model):
    __tablename__ = 'sensor'
    SensorID = db.Column(db.Integer, primary_key=True)
    minValue = db.Column(db.Integer)
    maxValue = db.Column(db.Integer)
    averageValue = db.Column(db.Integer)
    SensorNum = db.Column(db.Integer)
    SessionID = db.Column(db.Integer)

#SESSION MODEL
## TODO: fix data type to correct params
class Session(db.Model):
    __tablename__ = 'session'
    sessionID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    Session_Date = db.Column(db.Integer)
    Session_length = db.Column(db.Integer)

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

def session_serializer(session):
    return {
        'sessionID': session.sessionID,
        'userID': session.userID,
        'Session_Date': session.Session_Date,
        'Session_length': session.Session_length
    }

def sensor_serializer(sensor):
    return {
        'SensorID': sensor.SensorID,
        'minValue': sensor.minValue,
        'maxValue': sensor.maxValue,
        'averageValue': sensor.averageValue,
        'SensorNum': sensor.SensorNum,
        'SessionID': session.SessionID
    }

#getting all users
@app.route('/users')
def getUsers():
    try:
        #astriks unpacks map into array
        return jsonify([*map(user_serializer, User.query.all())])
    except Exception as e:
        print("\nThe error:\n" + str(e) + "\n")
        return jsonify({'Message': 'Error getting users'})


#handing login request
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            #change request byte object into a dict
            req_data = ast.literal_eval(request.data.decode('utf-8'))
            #get the user with matching email in DB
            user_to_validate = User.query.filter(User.Email==req_data['email']).first()
            if not user_to_validate:
                return {"Message": "User not found"}
            if user_to_validate.password == req_data['password']:
                return {'userID': user_to_validate.userID,
                        'username': user_to_validate.Email,
                        'isPhysio': user_to_validate.isPhysio}
            else:
                return {'Message':'LOGIN INVALID'}
        except:
            raise Exception("Cannot login user")
            return {'Message':'Cannot login user'}
    else:
        return {'Message':'Expected post'}

#getting the logged in users sessions
@app.route('/sessions', methods=['GET', 'POST'])
def getSessions():
    if request.method == 'POST':
        try:
            #change request byte object into a dict for userID
            req_data = ast.literal_eval(request.data.decode('utf-8'))
            userID = req_data["userID"]
            return jsonify([*map(session_serializer, Session.query.filter(Session.userID == userID))])
        except:
            raise Exception("Cannot get users sessions")
            return {'Message':'Cannot get users sessions'}
    else:
        return {'Message':'Expected post'}

#getting the sensor data for a session
@app.route('/sensors', methods=['GET', 'POST'])
def getSensorData():
    if request.method == 'POST':
        try:
            #change request byte object into a dict for userID
            req_data = ast.literal_eval(request.data.decode('utf-8'))
            sessionID = req_data["sessionID"]
            return jsonify([*map(sensor_serializer, Sensor.query.filter(Sensor.sessionID == sessionID))])
        except:
            raise Exception("Cannot get sensor data for session")
            return {'Message':'Cannot get sensor data for session'}
    else:
        return {'Message':'Expected post'}

if __name__ == '__main__':
    app.run(debug=True)
