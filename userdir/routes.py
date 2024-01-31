from db import models, schemas
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from userdir.usercrud import CRUD

router = Blueprint('userdir', __name__)
bcrypt = models.bcrypt

@router.route("/login/", methods = ['GET','POST'])
def login():
    credentials = schemas.LoginCred(**request.get_json())   # Gets the login credentials
    login = CRUD(email = credentials.email, password = credentials.password)
    token = login.get_token()
    return token


# all the activities are contolled by admin so only admins can create admin or user accounts
@router.route("/register/admin/", methods = ['GET', 'POST'])
@jwt_required()
def admin_register():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    user_data = schemas.UserDetails(**request.get_json())  # Gets the details of admin
    register_admin = CRUD(email = user_data.email, name = user_data.name, password = user_data.password)
    response = register_admin.register_admin()
    return response

@router.route("/register/user/", methods = ['GET', 'POST'])
@jwt_required()
def user_register():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    user_data = schemas.User(**request.get_json())  # Gets the details of user
    register_user = CRUD(email = user_data.email, name = user_data.name)
    response = register_user.register_user()
    return response

@router.route("/get/users/", methods = ['GET'])
@jwt_required()
def get_users():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    user = CRUD(email = user.email)
    response = user.get_all_users()
    return response

@router.route("/<int:userid>/user/details")
@jwt_required()
def get_user_details(userid):
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    user = CRUD(email = user.email)
    response = user.get_user_details(userid)
    return response