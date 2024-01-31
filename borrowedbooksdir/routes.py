from db import models, schemas
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from borrowedbooksdir.bbcrud import CRUD

bbrouter = Blueprint('borrowedbooksdir', __name__)
app = models.app
db = models.db

@bbrouter.route("/borrow/", methods = ['GET', 'POST'])
@jwt_required()
def borrow_books():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    borrow_data = schemas.BorrowedBooks(**request.get_json())
    borrow = CRUD(useremail = borrow_data.useremail, bookid = borrow_data.bookid)
    response = borrow.borrow_book()
    return response

@bbrouter.route("/return/", methods = ['PATCH'])
@jwt_required()
def return_book():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    borrow_data = schemas.BorrowedBooks(**request.get_json())
    borrow = CRUD(useremail = borrow_data.useremail, bookid = borrow_data.bookid)
    response = borrow.return_book()
    return response

@bbrouter.route("/borrowed/books/", methods = ['GET'])
@jwt_required()
def get_borrowedbooks():
    user = current_user
    if not user:
        return jsonify({ "error": "Unauthorized attempt to access" }), 404
    borrow = CRUD()
    response = borrow.get_list()
    return response