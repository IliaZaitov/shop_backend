from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()

class Good(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float(), nullable=False)
    max_quantity = db.Column(db.Integer(), nullable=False)

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

#add class Cart