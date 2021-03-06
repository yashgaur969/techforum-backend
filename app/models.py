from app import db


# model for creating a new user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email_id = db.Column(db.String())
    password = db.Column(db.String())
    designation = db.Column(db.String())
    dob = db.Column(db.String())
    mobile = db.Column(db.String())


# for creating a new question
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    answer = db.Column(db.String())
    first_name = db.Column(db.String())


class AccessTokenTable(db.Model):
    access_token = db.Column(db.String(), primary_key=True)
