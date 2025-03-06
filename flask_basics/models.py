from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # 创建db对象


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)



class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 反向引用
    author = db.relationship("User", backref="articles")



