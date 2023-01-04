from flask import Flask, request, render_template,Response,redirect,jsonify
from datacollect import datacollector
from trainer import trainer
from recog import recog
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import pymongo

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'mongodb+srv://saikiran:Epm9durTM8SzJcg@cluster0.s2wlw.mongodb.net/attendence_db',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    branch = db.StringField()
    phoneno = db.StringField()
    password = db.StringField()
    count = db.StringField()
    def to_json(self):
        return {"name": self.name}

@app.route("/")
def index1():
    return "Hello World!"
   
@app.route("/signup",methods = ['GET'])
def index():
    return render_template('signup.html')
 
@app.route('/signup', methods=['POST'])
def form_example():
    name=request.form.get('name')
    branch = request.form.get('branch')
    phoneno = request.form.get('phoneno')
    password = request.form.get('password')
    user = User(name = name,branch = branch,phoneno = phoneno,password = password,count="0")
    user.save()
    datacollector(phoneno)
    return redirect("/train")

@app.route('/train', methods=['GET'])
def train1():
    return render_template("train.html")

@app.route('/train', methods=['POST'])
def train():
    trainer()
    return redirect("/recog")

@app.route('/recog', methods=['GET'])
def recog1():
    return render_template('recog.html')

@app.route('/recog', methods=['POST'])
def recog2():
    recog()
    return redirect("/attendence")

@app.route("/attendence",methods=['GET'])
def attendence():
    return render_template("details.html")

@app.route("/attendence",methods = ['POST'])
def attendence1():
    phoneno=request.form.get('username')
    x = extract(str(phoneno))
    name = x['name']
    branch = x['branch']
    phoneno = x['phoneno']
    count = x['count']
    details = {"name":name,"branch":branch,"phoneno":phoneno,"attendence":count}
    return render_template('attendenceview.html',details = details)

def extract(phoneno):
    myclient = pymongo.MongoClient("mongodb+srv://saikiran:Epm9durTM8SzJcg@cluster0.s2wlw.mongodb.net")
    mydb = myclient["attendence_db"]
    mycol = mydb["user"]
    myquery = { "phoneno":phoneno }
    mydoc = mycol.find(myquery)
    print("working app extract")
    print(mydoc[0])
    return mydoc[0]

app.run()

