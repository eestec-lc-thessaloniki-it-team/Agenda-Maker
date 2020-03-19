import flask,os
from flask import request
from Flask.DemoClasses import Person



app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello It team</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route("/user",methods=['GET'])
def user():
    tasos = Person(19, "mail", "Tasos")
    return tasos.makeJson()

@app.route("/create-user",methods=['POST'])
def createUser():
    print(request.json)

    xarh=Person(request.json.get("age"),request.json.get("name"),request.json.get("gender"))
    print(xarh.makeJson()) # add database
    return 200

app.run()