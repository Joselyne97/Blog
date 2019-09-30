from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class Quotes:
    def __init__(self,id,author,quote,permalink):
        self.id=id
        self.author=author
        self.quote=quote
        self.link="http://quotes.stormconsultancy.co.uk/quotes/31"
    
    def hello(self):
        self.s = requests.Session()
        self.s.headers.update()
        return True

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    # upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
    # downvotes = db.relationship('Downvote', backref = 'user', lazy = 'dynamic')
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    
    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    
    comments = db.relationship('Comment',backref='blog',lazy='dynamic')
   
    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return blogs

    def __repr__(self):
        return f'Blog {self.description}'

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def update_blog(self):
        db.session.add(self)
        db.session.commit()

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Blog {self.description}'

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)
    
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

class Subscribe(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'User {self.name}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

