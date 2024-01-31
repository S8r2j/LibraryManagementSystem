import datetime
from config import setting
from flask import jsonify
from db import models
from flask_jwt_extended import create_access_token,JWTManager

# inheriting flask application from db.models
app = models.app

app.config['JWT_SECRET_KEY'] = setting.SECRET_KEY   # configuring secret key for creating tokens
jwt = JWTManager(app)   # For APIs to be used by any frontends

class Token:
    def create_token(self, identity):
        try:
            # identity validating
            if not identity:
                raise ValueError("Identity is missing")
            token = create_access_token(identity = identity, expires_delta = datetime.timedelta(minutes = 300))
            return token
        except ValueError as e:
            # handels the identity missing like specific errors
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            # for handeling all unexpected errors
            return jsonify({"error":"Failed to create the access token"}),500

# Tells the JWT Extended what identifier to include in token
@jwt.user_identity_loader
def user_identity_lookup(id):
    return id

# Retrieves the identity stored in JWT
@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    id = jwt_data["sub"]
    try:
        with app.app_context():
            user = models.User.query.join(models.Login).filter(models.Login.logid == id).first()
            if user is None:
                raise Exception("User not found")
            return user
    except Exception as e:
        app.logger.error(f"Error while fetching user:{str(e)}") # For debugging purposes
        raise Exception("Error while fetching user")