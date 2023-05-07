from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, current_user

from models import db, Good, User, Cart

app = Flask(__name__)

app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(pk):
    return User.query.filter_by(id=pk).first()

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
    if request.method == "POST":
        name = request.json['name']
        price = request.json['price']
        quantity = request.json['quantity']
        good = User.query.filter_by(name=name).first()
        if good:
            return jsonify({"error": "Good already exists"})
        good = Good(name, price, quantity)
        db.session.add(good)
        db.session.commit()
        return jsonify({"message": "Good created successfully"})


@app.route("/api/good/<g_id>", methods = ["get","put","delete"])
def good_instance_page(g_id):
    if request.method == "GET":
        good = Good.query.filter_by(id=g_id).first()
        return good.json
    if request.method == "DELETE":
        if current_user.is_admin:
            good = Good.query.filter_by(id=g_id).first_or_404()
            db.session.delete(good)
            db.session.commit()
            return jsonify({"message": "Good deleted successfully"})
        else:
            return jsonify({"error": "Admin only"})
    if request.method == "PUT":
        if current_user.is_admin:
            name = request.json['name']
            price = request.json['price']
            description = request.json['description']
            quantity = request.json['quantity']
            good = Good.query.filter_by(id=g_id).first_or_404()
            good.name = name
            good.price = price
            good.description = description
            good.max_quantity = quantity
            db.session.add(good)
            db.session.commit()
            return jsonify({"message": "Good updated successfully"})
        else:
            return jsonify({"error": "Admin only"})

@app.route("/api/user", methods=["post", 'get'])
def users_page():
    if request.method == "GET":
        users = User.query.all()
        userlist=[]
        for user in users:
            userlist.append(user.json)
        return jsonify(userlist)
    if request.method == "POST":
        username=request.json['username']
        email=request.json['email']
        password=request.json['password']
        pass_confirm=request.json['pass_confirm']
        user = User.query.filter_by(login=username).first()
        if user:
            return jsonify({"error":"Username already exists"})
        user = User.query.filter_by(mail=email).first()
        if user:
            return jsonify({"error": "Email already registered"})
        if pass_confirm!=password:
            return jsonify({"error": "Password not confirmed"})
        user = User(username,email,password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"})


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
    # добавить метод PUT
    # В них реализовать изменение пользователя
    # Святослав


@app.route("/api/cart", methods=["post",'get'])
def carts_page():
    if request.method == "GET":
        carts = Cart.query.all()
        cartlist=[]
        for cart in carts:
            cartlist.append(cart.json)
        return jsonify(cartlist)
    #if request.method == "POST":
    #методы POST

#endpoint "/api/cart/id"
#Александр
@app.route('/api/cart/<c_id>', methods=['put','get','delete'])
def cart_page(c_id):
    cart = Cart.query.filter_by(id=c_id).first_or_404()
    if request.method == "PUT":
        if cart.user_id == current_user:
            good_id = request.json['good_id']
            quantity = request.json['quantity']
            cart.quantity = quantity
            cart.good_id = good_id
            db.session.add(cart)
            db.session.commit()
            return jsonify({"message": "Cart updated successfully"})
        else:
            return jsonify({"error": "Admin only"})
app.run(debug=True)