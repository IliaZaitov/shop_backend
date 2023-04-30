from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models import db, Good, User, Cart

app = Flask(__name__)

app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

cors = CORS(app)


@app.before_first_request
def bfr():
    db.drop_all()
    db.create_all()
    good1=Good("Губозакаточная машинка",20000,10)
    good2 = Good("Карточки с видом на закат губы", 200, 3)
    good3 = Good("Игральные контурные карты", 500, 40)
    good1.description = "Особо мощная машина, закатывает даже широко раскатанные губы"
    db.session.add(good1)
    db.session.add(good2)
    db.session.add(good3)
    db.session.commit()
    user1 = User('Login', 'Mail', 'Password')
    user2 = User('Admin', 'Admin@mail.ru', 'Admin')
    user2.is_admin=True
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    cart1 = Cart(good1.id,user1.id,2)
    db.session.add(cart1)
    db.session.commit()



@app.route("/api/good", methods=["post",'get'])
def good_page():
    if request.method == "GET":
        goods = Good.query.all()
        listgoods=[]
        for good in goods:
            listgoods.append(good.json)
        return jsonify(listgoods)

@app.route("/api/good/<g_id>", methods = ["get","put","delete"])
def good_instance_page(g_id):
    if request.method == "GET":
        good = Good.query.filter_by(id=g_id).first()
        return good.json


@app.route("/api/user", methods=["post",'get'])
def users_page():
    if request.method == "GET":
        users = User.query.all()
        userlist=[]
        for user in users:
            userlist.append(user.json)
        return jsonify(userlist)
    #if request.method == "POST":

@app.route("/api/user/<u_id>", methods=["put",'get','delete'])
def user_page(u_id):
    if request.method == "GET":
        user = User.query.filter_by(id=u_id).first()
        if user:
            return user.json
        else:
            return jsonify({"message":"User not found"})
    if request.method == "DELETE":
        user = User.query.filter_by(id=u_id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return 'Пользователь удален'


@app.route("/api/cart", methods=["post",'get'])
def carts_page():
    if request.method == "GET":
        carts = Cart.query.all()
        cartlist=[]
        for cart in carts:
            cartlist.append(cart.json)
        return jsonify(cartlist)
    #if request.method == "POST":

app.run(debug=True)