from flask import Flask
from core.config import setting
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)   # Initialization of flask application
# setting up the database uri for establishing connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{setting.DATABASE_USER}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOST}/{setting.DATABASE_NAME}'


db = SQLAlchemy(app)    # Initializing SQLAlchemy for flask instance to setup database
bcrypt = Bcrypt(app)    # Initializing Bcrypt for password hashing
class User(db.Model):
    userid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    membershipdate = db.Column(db.DateTime, default  = datetime.utcnow(), nullable = False)
    borrowedbooks = db.relationship('BorrowedBooks', backref = 'user', lazy = True)
    login = db.relationship('Login', back_populates = 'user', uselist = False, cascade = "all, delete-orphan")

class Login(db.Model):
    logid = db.Column(db.Integer, primary_key =True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)
    user = db.relationship("User", back_populates = 'login')

class Book(db.Model):
    sn = db.Column(db.Integer, primary_key = True, autoincrement = True)
    bookid = db.Column(db.String(50), unique = True, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    isbn = db.Column(db.String(50), nullable = False)
    publisheddate = db.Column(db.Date, nullable = False)
    genre = db.Column(db.String(150), nullable = False)
    bookdetails = db.relationship('BookDetails', backref = 'book', uselist = False, lazy = True)

class BookDetails(db.Model):
    detailsid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    bookid = db.Column(db.String(50), db.ForeignKey('book.bookid'), nullable = False, unique = True)
    numberofpages = db.Column(db.Integer, nullable = False)
    publisher = db.Column(db.String(255), nullable = False)
    language = db.Column(db.String(50), nullable = False)

class BorrowedBooks(db.Model):
    sn = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable = False)
    bookid = db.Column(db.String(50), db.ForeignKey('book.bookid'), nullable = False)
    borrowdate = db.Column(db.Date, default = datetime.utcnow(), nullable = False)
    returndate = db.Column(db.Date, nullable = True)


# creating all the models in the database
with app.app_context():
    db.create_all()
    user = User.query.all()
    # Initializing the admin since they are the ones to do operations
    if len(user) == 0:
        try:
            with app.app_context():
                user = User(name = "Admin", email = "admin@gmail.com")
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)
                user = User.query.first()
                login = Login(userid = user.userid, password = f"{bcrypt.generate_password_hash('admin@123').decode('utf-8')}")
                db.session.add(login)
                db.session.commit()
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")