from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import or_

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique = True)
    name = db.Column(db.String(50),unique = True)
    email = db.Column(db.String(50),unique = True)
    phone = db.Column(db.Integer,unique = True)
    password = db.Column(db.String(100))

#Route to get all the users 
@app.route('/api/v1/users',methods = ['GET'])
def get_all_users():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['phone'] = user.phone
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users' : output})


@app.route('/api/v1/login',methods = ['GET','POST'])
def get_user():
    data = request.get_json()
    user = User.query.filter(User.name == data['name']).first()
    user_data = {}


    if not user:
        return jsonify({'message':'User does not exist'})
    else:
        user_data['name'] = user.name
        user_data['public_id'] = user.public_id
        user_data['email'] = user.email
        user_data['phone'] = user.phone
        user_data['password'] = user.password

    return jsonify(user_data)


#Route to get a single the user
@app.route('/api/v1//user/<name>',methods = ['GET'])
def get_one_user(name):

    user = User.query.filter_by(name = name).first()

    if not user:
        return jsonify({'message':'User does not exist'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['email'] = user.email
    user_data['phone'] = user.phone
    user_data['password'] = user.password

    return jsonify(user_data)

@app.route('/api/v1/register',methods = ['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method = 'sha256')
    new_user = User(public_id = str(uuid.uuid4()),name = data['name'],email = data['email'],phone = data['phone'],password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"data":{"message":"user sucessfully created",
                    "isSuccess": "true",},"code": "200"})

@app.route('/user/<public_id>',methods = ['PUT'])
def change_user_details(public_id):
    return ''

@app.route('/user/<public_id>',methods = ['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id = public_id).first()

    if not user:
        return jsonify({'message':'User does not exist'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'User deleted Sucessfully'})

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
