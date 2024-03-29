import datetime

from sqlalchemy import text

from exts import db

UserCollection_table = db.Table('collection',
                                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usernumber = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), default='images/mudkip.png')

    postses = db.relationship('Posts', secondary=UserCollection_table,
                              backref=db.backref('users'),
                              lazy='dynamic')


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    # now is the value from this function
    # now() is to call this function
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # users = db.relationship('User', secondary=UserCollection_table,
    #                         backref=db.backref('postses'),
    #                         lazy='dynamic')
    author = db.relationship('User', backref=db.backref('posts'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100), nullable=False)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    posts = db.relationship('Posts', backref=db.backref('comments', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('comments'))
