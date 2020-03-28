import flask, os
from flask import request, jsonify
from Flask.DemoClasses import Person
from mongo.exampleMongoConnection import *

from BasicClasses.Agenda import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
connectToMongo = connectMongo()
print(APP_ROOT)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello It team</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route("/create-agenda", methods=['POST'])
def createAgenda():
    """
    In request I expect date, lc
    :return: object Agenda + response
    """
    objectAgenda = getAgendaFromJson(connectToMongo.createNewAgenda(request.json))
    return jsonify(response=200, agenda=objectAgenda.makeJson())


@app.route("/get-agenda-id", methods=['GET'])
def getAgendaByID():
    """
    In request I expect a string of ID
    :return: a object agenda as json + response
    """
    objectAgenda = getAgendaFromJson(connectToMongo.getAgendaById(request.json.get("id")))
    return jsonify(response=200, agenda=objectAgenda.makeJson())


@app.route("/create-user", methods=['POST'])
def createUser():
    print(request.json)

    xarh = Person(request.json.get("age"), request.json.get("name"), request.json.get("gender"))
    print(xarh.makeJson())  # add database
    return 200


app.run()
