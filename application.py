import os
from flask import Flask, request
from flask_cors import CORS
import sqlalchemy
app = Flask(__name__)
CORS(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import jwt
import traceback

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
import models
models.db.init_app(app)

# -------------------------------------test-----------------------------------------
def root():
    return {
        "message": "ok for boOk House"
        }
app.route('/', methods=["GET"])(root)

# -------------------------------------DB users table-----------------------------------------
def create_user():
    hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode('utf-8')
    try:
        user = models.User(
        email=request.json["email"],
        # password=request.json["password"]
        password=hashed_pw
        )
        models.db.session.add(user)
        models.db.session.commit()
        # encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
        return {
        "user": user.to_json(), 
        "user_id": user.id 
        }
    except sqlalchemy.exc.IntegrityError:
        return { "message": "Email must be present and unique"}, 400
app.route('/signup', methods=["POST"])(create_user)

def login():
    user = models.User.query.filter_by(email=request.json["email"]).first()
    if not user: 
        return { "message": "User not found"}, 404
    # if user.password == request.json["password"]:
    if bcrypt.check_password_hash(user.password, request.json["password"]):
        # encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
        return {
        "user": user.to_json(),
        "user_id": user.id
        }
    else:
        return { "message": "Password incorrect" }, 401 
app.route('/login', methods=["POST"])(login)


def verify_user():
    decrypted_id = jwt.decode(request.headers['Authorization'], os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    ["user_id"]
    # user = models.User.query.filter_by(id=request.headers["Authorization"]).first()
    user = models.User.query.filter_by(id= decrypted_id['id']).first()
    if user: 
        return {"user": user.to_json()}
    else: 
        return { "message": "user not found" }, 404
    # if not user:
    #   return { "message": "user not found" }, 404
    # return { "user": user.to_json() }
app.route('/users/verify', methods=["GET"])(verify_user)

# -------------------------------------DB books table-----------------------------------------
def create_book():
    try:

        book = models.Book(
            title = request.json["title"],
            name = request.json["name"],
            cover = request.json["cover"],
            userId = request.json["userId"]
        )
        models.db.session.add(book)
        models.db.session.commit()
        return{
            "book":book.to_json()
        }
    except sqlalchemy.exc.IntegrityError:
        traceback.print_exc()
        return { "message": "book add error"}, 400
app.route('/book', methods=["POST"])(create_book)

def all_books(userId):
    books = models.Book.query.filter_by(userId=userId).all()
    return {"books":[b.to_json() for b in books]}
app.route('/books/user/<int:userId>', methods=["GET"])(all_books)

def delete_single_book(bookId):
    book = models.Book.query.filter_by(id=bookId).first()
    models.db.session.delete(book)
    models.db.session.commit()
    return{"book":book.to_json()}
app.route('/books/<int:bookId>', methods=["DELETE"])(delete_single_book)
# -------------------------------------DB comment table-----------------------------------------
def create_comment():
    try:
        comment = models.Comment(
            comment = request.json["comment"],
            bookId = request.json["bookId"],
        )
        models.db.session.add(comment)
        models.db.session.commit()
        return{
            "comment":comment.to_json()
        }
    except sqlalchemy.exc.IntegrityError:
        return { "message": "comment add error"}, 400
app.route('/comment', methods=["POST"])(create_comment)

def all_comments(bookId):
    comments = models.Comment.query.filter_by(bookId=bookId).all()
    return {"comments":[c.to_json() for c in comments]}
app.route('/comments/book/<int:bookId>', methods=["GET"])(all_comments)

def delete_single_comment(commentId):
    comment = models.Comment.query.filter_by(id=commentId).first()
    models.db.session.delete(comment)
    models.db.session.commit()
    return{"comment":comment.to_json()}
app.route('/comment/<int:commentId>', methods=["DELETE"])(delete_single_comment)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)