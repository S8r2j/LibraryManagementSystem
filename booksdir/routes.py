from db import models, schemas
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from booksdir.bookscrud import BookCRUD

bookrouter = Blueprint('booksdir',__name__)

# Adds the new books
@bookrouter.route("/books/", methods = ['GET', 'POST'])
@jwt_required()
def new_books():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    book_data = schemas.BookDetails(**request.get_json())
    book = BookCRUD(bookid = book_data.bookid,title = book_data.title, isbn = book_data.isbn, publisheddate = book_data.publisheddate, genre = book_data.genre,
                    numberofpages = book_data.numberofpages,publisher = book_data.publisher,language = book_data.language)
    response = book.new_books()
    return response

# Gets the list of the books
@bookrouter.route("/book/list/", methods = ['GET'])
@jwt_required()
def get_book_list():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    book = BookCRUD()
    response =book.get_bookList()
    return response

# get the details of the book
@bookrouter.route("/<string:bookid>/book/details/", methods = ['GET'])
@jwt_required()
def get_book_details(bookid):
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    book = BookCRUD()
    response = book.get_idbookdetails(bookid = bookid)
    return response

@bookrouter.route("/books/<bookid>", methods = ['PATCH'])
@jwt_required()
def update_details(bookid):
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    book_data = schemas.UpdateBooks(**request.get_json())
    book = BookCRUD(
        bookid = book_data.bookid, title = book_data.title, isbn = book_data.isbn,
        publisheddate = book_data.publisheddate, genre = book_data.genre,
        numberofpages = book_data.numberofpages, publisher = book_data.publisher, language = book_data.language
        )
    response = book.update_bookDetails()
    return response