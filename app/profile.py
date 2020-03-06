# from flask import jsonify
# from flask_jwt_extended import create_access_token
#
# from app import db
# from app.models import User
#
#
# def user_post(data):
#     user = User(first_name=data['first_name'], last_name=data['last_name'],
#                 email_id=data['email_id'], password=data['password'],
#                 designation=data['designation'], dob=data['dob'], mobile=data['mobile'])
#     db.session.add(user)
#     db.session.commit()
#     access_token = create_access_token(identity=user.email_id)
#     return jsonify(access_token=access_token)