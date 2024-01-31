import datetime
import json
from datetime import datetime
from db import models
from core.tokenop import tokens
from flask_jwt_extended import jwt_required, current_user
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

app = models.app
db = models.db

class CRUD:
    def __init__(self, bookid = None,  useremail = None,returndate = None):
        self.useremail = useremail
        self.bookid = bookid
        self.returndate = returndate

    # Lends user book to borrow
    @jwt_required()
    def borrow_book(self):
        try:
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            user = models.User.query.filter(models.User.email == self.useremail).first()
            if not user:
                return jsonify({"error":f"No user with {self.useremail} email address found"}), 404
            borrow = models.BorrowedBooks(userid = user.userid, bookid = self.bookid)
            with app.app_context():
                db.session.add(borrow)
                db.session.commit()
                return jsonify({"message":"User borrowed the book successfully"}), 200
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
            # handle the database errors
            return jsonify({ "error": f"Database error occurred i.e. {e}" }), 500
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": f"An unexpected error occurred,i.e. {e}" }), 500

    # Updates the return time of the borrowed book
    @jwt_required()
    def return_book(self):
        user = current_user
        if not user:
            return jsonify({ "error": "Unauthorized attempt to access" }), 404
        user = models.User.query.filter(models.User.email == self.useremail).first()
        borrow = models.BorrowedBooks.query.filter(models.BorrowedBooks.bookid == self.bookid).first()
        if not borrow:
            return jsonify({"error":"No borrowing found"}), 404
        self.returndate = datetime.utcnow()
        for key, value in vars(self).items():
            if hasattr(borrow, key) and getattr(borrow, key) != value and value is not None:
                setattr(borrow, key, value)

        try:
            db.session.commit()
            return jsonify({ "message": "Updated Successfully" }), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({ "error": f"Failed to update due to: {e}" }), 500

    # Gets the list of all the borrowed books
    @jwt_required()
    def get_list(self):
        user = current_user
        if not user:
            return jsonify({ "error": "Unauthorized attempt to access" }), 404
        books = models.Book.query.join(models.BorrowedBooks).all()
        borrowed_books = {}
        list = []
        for book in books:
            borrowed_books['Title'] = book.title
            borrowed_books['ISBN'] = book.isbn
            list.append(borrowed_books)
        return jsonify(list),200