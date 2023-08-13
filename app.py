from flask import *
from flask_cors import CORS
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import json
# from flask_migrate import Migrate, migrate
import MachineLearningModel
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

# migrate = Migrate(app, db)
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    spo2 = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"
@app.route("/",methods=['POST','GET'])
def calculate():
    img = request.files['image']
    img = Image.open(img)
    resEye,resYarn = MachineLearningModel.find(img)
    returner ={}
    returner['result'] = int(resEye)*0.3+int(resYarn)*0.7 if(resEye!=-1) else resYarn
    return returner
@app.route("/add",methods=['POST','GET'])
def addUser():
    first_name = request.json.get("fname")
    last_name = request.json.get("lname")
    age = request.json.get("age")
    spo2 = request.json.get("spo2")
    returner = {}
    print(first_name,last_name,age,spo2)
    if first_name != '' and last_name != '' and age is not None and spo2 is not None:
        p = user(first_name=first_name, last_name=last_name, age=age,spo2=spo2)
        db.session.add(p)
        db.session.commit()
        returner['status'] = "success"
    else:
        returner['status'] = "failure"
    return returner

@app.route("/select",methods=['POST','GET'])
def select():
    profile = user.query.all()
    user_list = []
    for users in profile:
        user_data = {
            'id': users.id,
            'first_name': users.first_name,
            'last_name': users.last_name,
            'age' : users.age,
            'spo2':users.spo2
        }
        user_list.append(user_data)

    return jsonify(user_list)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug=True)