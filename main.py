from flask import Flask, request, jsonify
from models import db, Good

app = Flask(__name__)

app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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



@app.route("/api/good", methods=["post",'get'])
def good_page():
    if request.method == "GET":
        goods = Good.query.all()
        listgoods=[]
        for good in goods:
            listgoods.append(good.json)
        return jsonify(listgoods)

app.run(debug=True)