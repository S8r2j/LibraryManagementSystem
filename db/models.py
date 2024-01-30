from flask import Flask
from core.config import setting
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)   # Initialization of flask application
# setting up the database uri for establishing connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{setting.DATABASE_USER}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOST}/{setting.DATABASE_NAME}'
app.config['SECRET_KEY'] = setting.SECRET_KEY

db = SQLAlchemy(app)    # Initializing SQLAlchemy for flask instance to setup database


# creating all the models in the database
with app.app_context():
    db.create_all()