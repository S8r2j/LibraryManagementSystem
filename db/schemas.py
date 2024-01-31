from pydantic import BaseModel, EmailStr    # using basemodel for data validations
from datetime import date

class User(BaseModel):
    name: str
    email : EmailStr

class Login(BaseModel):
    password : str

class UserDetails(User,Login):
    pass

class Book(BaseModel):
    title : str
    isbn : str
    publisheddate : date
    genre : str

class BookDetails(BaseModel):
    numberofpages : int
    publisher : str
    language : str

class BorrowedBooks(BaseModel):
    returndate : date
