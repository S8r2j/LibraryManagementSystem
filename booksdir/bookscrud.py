from db import models
from core.tokenop import tokens
from flask_jwt_extended import jwt_required, current_user
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

app = models.app
db = models.db

class BookCRUD:
    def __init__(self, bookid, title = None, isbn = None, publisheddate = None, genre = None,numberofpages = None, publisher = None, language = None):
        self.title = title
        self.isbn = isbn
        self.publisheddate = publisheddate
        self.genre = genre
        self.numberofpages = numberofpages
        self.language = language
        self.publisher = publisher
        self.bookid = bookid

    @jwt_required()
    def new_books(self):
        try:
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            existing_books = models.Book.query.filter(models.Book.isbn == self.isbn).first()
            if existing_books:
                return jsonify({"error":"This book is already registered"}), 409
            with app.app_context():
                new_book = models.Book(bookid = self.bookid,title = self.title, isbn = self.isbn, publisheddate = self.publisheddate, genre = self.genre)
                db.session.add(new_book)
                db.session.commit()
                book_details = models.BookDetails(bookid = self.bookid, numberofpages = self.numberofpages, language = self.language, publisher = self.publisher)
                db.session.add(book_details)
                db.session.commit()
                return jsonify({"message":"New Book Added"})
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
            # handle the database errors
            return jsonify({ "error": f"Database error occurred i.e. {e}" }), 500
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": f"An unexpected error occurred,i.e. {e}" }), 500

    @jwt_required()
    def get_bookList(self):
        try:
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            book_list = models.Book.query.all()
            list = []
            for book in book_list:
                list.append({"book":f"{book}"})
            return jsonify(list),200
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
            # handle the database errors
            return jsonify({ "error": f"Database error occurred i.e. {e}" }), 500
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": f"An unexpected error occurred,i.e. {e}" }), 500

    @jwt_required()
    def get_idbookdetails(self,bookid):
        try:
            user = current_user
            if not user:
                return jsonify({ "error": "Unauthorized attempt to access" }), 404
            book = models.Book.query.filter(models.Book.bookid == bookid).first()
            if not book:
                return jsonify({"error":"No book found"}), 404
            details_dict = {}
            details_dict['bookid'] = book.bookid
            details_dict['title'] = book.title
            details_dict['isbn'] = book.isbn
            details_dict['published date'] = book.publisheddate
            details_dict['genre'] = book.genre

            if book.bookdetails:
                details_dict['number of pages'] = book.bookdetails.numberofpages
                details_dict['publisher'] = book.bookdetails.publisher
                details_dict['language'] = book.bookdetails.language
            return jsonify(details_dict), 200
        except SQLAlchemyError as e:
            # Logging the error for debugging
            app.logger.error(f"Database error: {e}")
            # handle the database errors
            return jsonify({ "error": f"Database error occurred i.e. {e}" }), 500
        except Exception as e:
            # Catch all the unexpected errors
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({ "error": f"An unexpected error occurred,i.e. {e}" }), 500

    # update the values of fields that are only updated
    @jwt_required()
    def update_bookDetails(self):
        user = current_user
        if not user:
            return jsonify({ "error": "Unauthorized attempt to access" }), 401

        book = models.Book.query.filter_by(bookid = self.bookid).first()
        if book is None:
            return jsonify({ "error": "Book not found" }), 404

        for key, value in vars(self).items():
            if hasattr(book, key) and getattr(book, key) != value and value is not None:
                setattr(book, key, value)

        try:
            db.session.commit()
            return jsonify({ "message": "Updated Successfully" }), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({ "error": f"Failed to update due to: {e}" }), 500