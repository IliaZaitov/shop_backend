from flask_sqlalchemy import  SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

class Good(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique = True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float(), nullable=False)
    max_quantity = db.Column(db.Integer(), nullable=False)
    cart_id = db.relationship('Cart',backref='cart')

    def __init__(self,name,price,quantity):
        self.name = name
        self.price = price
        self.max_quantity = quantity

    @property
    def json(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state')
        return dictionary

#add class User
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    login = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Boolean())
    cart_id = db.relationship('Cart',backref='in_cart')

    def __init__(self, username, email, password):
        self.login = username
        self.mail = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def json(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state')
        return dictionary

#add class Cart
class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer(), primary_key=True)
    good_id = db.Column(db.Integer(),db.ForeignKey('goods.id'))
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    quantity = db.Column(db.Integer())

    def __init__(self,good_id,user_id,quantity):
        self.good_id = good_id
        self.user_id = user_id
        self.quantity = quantity

    @property
    def json(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state')
        return dictionary