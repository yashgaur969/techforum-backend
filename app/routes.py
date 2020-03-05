from os import abort
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import app, db
from app.models import User, Card, AccessTokenTable


@app.route('/hello-world')
def hello_world():
    return "hello world"


@app.route('/users/signup', methods=['POST'])
def new_user():
    if request.method == 'POST':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email_id = request.json.get('email_id')
        password = request.json.get('password')
        designation = request.json.get('designation')
        dob = request.json.get('dob')
        mobile = request.json.get('mobile')
        if first_name is None or password is None or email_id is None:
            abort()
        if User.query.filter_by(first_name=first_name).first() is not None:
            abort()
        user = User(first_name=first_name, last_name=last_name,
                    email_id=email_id, password=password, designation=designation, dob=dob, mobile=mobile)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.email_id)
        return jsonify(access_token=access_token)


@app.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email_id = request.json.get('email_id')
        password = request.json.get('password')
        user = User.query.filter_by(email_id=email_id).first()
        if not user:
            return 'user with email {} does not exist'.format(email_id)
        if password == user.password:
            access_token = create_access_token(identity=user.email_id)
            access = AccessTokenTable(access_token=access_token)
            db.session.add(access)
            db.session.commit()
            return jsonify(access_token=access_token)
        else:
            return 'wrong credentials'


@app.route('/dashboard', methods=['POST', 'GET'])
def card():
    if request.method == 'POST':
        question = request.json.get('question')
        answer = request.json.get('answer')
        cards = Card(question=question, answer=answer)
        db.session.add(cards)
        db.session.commit()
        return "new question is created"
    if request.method == 'GET':
        cards = Card.query.all()
        card_object = [{"question": s.question, "answer": s.answer} for s in cards]
        return {'data': card_object}


@app.route('/info/<email_id>', methods=['POST', 'GET'])
def user_info(email_id):
    if request.method == 'GET':
        user = User.query.filter_by(email_id=email_id).first()
        


