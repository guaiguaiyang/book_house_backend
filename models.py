from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String)

  def to_json(self):
    return {
      "id": self.id,
      "email": self.email
    }


class Book(db.Model):
  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  name = db.Column(db.String)
  cover = db.Column(db.String)
  userId = db.Column(db.Integer,db.ForeignKey('users.id'))
  
  def to_json(self):
    return {
      "id": self.id,
      "title":self.title,
      "name":self.name,
      "cover":self.cover,
      "userId":self.userId
    }

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.String)
  title = db.Column(db.String)
  bookId = db.Column(db.Integer,db.ForeignKey('books.id'))
  
  def to_json(self):
    return {
      "id": self.id,
      "comment":self.comment,
      "title":self.title,
      "bookId":self.bookId
    }