from db import models
from core.tokenop import tokens
from flask_jwt_extended import jwt_required, current_user
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

app = models.app
db = models.db
bcrypt = models.bcrypt

class CRUD:
    def __init__(self, email, name = None, password=None):
        self.email = email
        self.name = name
        self.password = password

    def get_token(self):
        user = models.User.query.filter(models.User.email == self.email).first()
        if user and user.login:
            # checking if the password matches or not
            if bcrypt.check_password_hash(user.login.password, self.password):
                tkn = tokens.create_token(identity = user.login.logid)
                print(tkn)
                return tkn

    def register(self):
        try:
            with app.app_context():
                existing_user = models.User.query.filter(models.User.email == self.email).first()
                if existing_user:
                    return jsonify({ "error": "User with this email already exists" }), 400
                user = models.User(name = self.name, email = self.email)
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)
                user = models.User.query.filter(models.User.email == self.email).first()
                return user.userid
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
            # handle the database errors
            return jsonify({ "error": "Database error occurred" }), 500
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": "An unexpected error occurred" }), 500

    # Register users only
    @jwt_required()
    def register_user(self):
        user = current_user
        if not user:
            return jsonify({ "error": "Unauthorized attempt to access" }), 404
        id = self.register()
        if isinstance(id, int):
            return jsonify({"message": "User Registered" }),200
        return id

    # Registering admins only
    @jwt_required()
    def register_admin(self):
        user = current_user
        if not user:
            return jsonify({ "error": "Unauthorized attempt to access" }), 404
        id = self.register()
        if isinstance(id,int):
            try:
                with app.app_context():
                    existing_user = models.User.query.filter(models.User.email == self.email).first()
                    if not existing_user:
                        return jsonify({ "error": "No user found with the email" }), 400
                    hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
                    login_details = models.Login(userid = id, password = hashed_password)
                    db.session.add(login_details)
                    db.session.commit()
                    return jsonify({"message":"Admin Registered"}), 200
            except SQLAlchemyError as e:
                # Logging the error for debugging
                app.logger.error(f"Database error: {e}")
                # handle the database errors
                return jsonify({ "error": "Database error occurred" }), 500
            except Exception as e:
                # Catch all the unexpected errors
                app.logger.error(f"Unexpected error: {e}")
                return jsonify({ "error": "An unexpected error occurred" }), 500
        return id


    @jwt_required()
    def get_all_users(self):
        try:
            # checking the user is authorized admin
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            user_list = []
            users = models.User.query.all()
            for user in users:
                user_dict = { }
                user_dict['Name'] = user.name
                if user.login:
                    user_dict['Role'] = "Admin"
                else:
                    user_dict['Role'] = "User"
                user_list.append(user_dict)
            return jsonify(user_list),200
        except SQLAlchemyError as e:
            app.logger.error(f"Database error: {e}")
            return jsonify({ "error": "Database error occurred" }), 500
        except Exception as e:
            # Handle other unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": "An unexpected error occurred" }), 500

    @jwt_required()
    def get_user_details(self, id):
        try:
            # checking the user is authorized admin
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            users = models.User.query.filter(models.User.userid == id).first()
            user_dict = { }
            user_dict['Name'] = users.name
            user_dict['Email'] = users.email
            if users.login:
                user_dict['Role'] = "Admin"
            else:
                user_dict['Role'] = "User"

            return jsonify(user_dict),200
        except SQLAlchemyError as e:
            app.logger.error(f"Database error: {e}")
            return jsonify({ "error": "Database error occurred" }), 500
        except Exception as e:
            # Handle other unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": "An unexpected error occurred" }), 500