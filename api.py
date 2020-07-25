from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    public_id = db.Column(db.String(50),unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))


@app.route('/user',methods = ['GET'])
def get_all_users():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users' : output})

@app.route('/user/<public_id>',methods = ['GET'])
def get_one_user(public_id):

    user = User.query.filter_by(public_id = public_id).first()

    if not user:
        return jsonify({'message':'User does not exist'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password

    return jsonify({'user':user_data})

@app.route('/user',methods = ['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method = 'sha256')
    new_user = User(public_id = str(uuid.uuid4()),name = data['name'],password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'New User Created'})

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
    app.run(debug = True)