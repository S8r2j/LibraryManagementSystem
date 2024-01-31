from pydantic import BaseModel, EmailStr    # using basemodel for data validations
from datetime import date
from typing import Optional

class User(BaseModel):
    name: str
    email : EmailStr

class Login(BaseModel):
    password : str

class UserDetails(User,Login):
    pass

class LoginCred(Login):
    email: EmailStr
class Book(BaseModel):
    bookid: str
    title : str
    isbn : str
    publisheddate : date
    genre : str

class BookDetails(Book):
    numberofpages : int
    publisher : str
    language : str

class UpdateBooks(BaseModel):
    bookid: Optional[str] = None
    title: Optional[str]= None
    isbn: Optional[str]= None
    publisheddate: Optional[date] = None
    genre: Optional[str]= None
    numberofpages: Optional[int]= None
    publisher: Optional[str]= None
    language: Optional[str]= None
class BorrowedBooks(BaseModel):
    bookid: str
    useremail: Optional[EmailStr] = None
    returndate : Optional[date] = None