from os import abort
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app import app, db
from app.models import User, Card, AccessTokenTable


@app.route('/hello-world')
def hello_world():
    return "hello world"


# to create a new user
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
                    email_id=email_id, password=password,
                    designation=designation, dob=dob, mobile=mobile)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.email_id)
        return jsonify(access_token=access_token)


# for a particular user to login
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
            first_name = user.first_name
            return jsonify(access_token=access_token,
                           email_id=email_id, first_name=first_name)
        else:
            return 'wrong credentials'


# when a particular user post a card
@app.route('/dashboard/page/<int:page>')
@app.route('/dashboard', methods=['POST', 'GET'])
def card(page=1):
    if request.method == 'POST':
        question = request.json.get('question')
        answer = request.json.get('answer')
        first_name = request.json.get('first_name')
        cards = Card(question=question, answer=answer,
                     first_name=first_name)
        db.session.add(cards)
        db.session.commit()
        return "new question is created"
    if request.method == 'GET':
        cards = Card.query.paginate(page, 20, False).items
        card_object = [{"question": s.question, "answer": s.answer,
                        "first_name": s.first_name} for s in cards]
        return {'data': card_object}


# fetching user info using email_id
@app.route('/info/<email_id>', methods=['GET'])
def user_info(email_id):
    if request.method == 'GET':
        user = User.query.filter_by(email_id=email_id)
        user_object = [
            {"first_name": s.first_name, "last_name": s.last_name,
             "designation": s.designation, "email_id": s.email_id,
             "mobile": s.mobile, "dob": s.dob} for s in user]
        return {'data': user_object}


# fetching the post of a particular user
@app.route('/user/posts/<first_name>', methods=['POST', 'GET'])
def user_post(first_name):
    if request.method == 'GET':
        user_cards = Card.query.filter_by(first_name=first_name)
        usercard_object = [{"question": s.question,
                            "answer": s.answer, "first_name": s.first_name}
                           for s in user_cards]
        return {'data': usercard_object}