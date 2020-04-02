import flask, os
from flask import request, jsonify
from Flask.DemoClasses import Person
from mongo.connectMongo import *

from BasicClasses.Agenda import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
connectToMongo = connectMongo()  # connection to mongo
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
    responseWrapper: ResponseWrapper = connectToMongo.createNewAgenda(request.json)
    return jsonify(response=200, agenda=responseWrapper.object.makeJson())


@app.route("/get-agenda-id", methods=['GET'])
def getAgendaByID():
    """
    In request I expect a string of ID
    :return: a object agenda as json + response
    """
    objectAgenda = getAgendaFromJson(connectToMongo.getAgendaById(request.json.get("id")))
    return jsonify(response=200, agenda=objectAgenda.makeJson())


@app.route("/create-section", methods=['POST'])
def createSection():
    """
    In request I expect agenda_id, section_name, maybe position
    :return:
    """
    # first check if everything we need is there
    print(request)
    data = request.json
    if "id" in data and "section_name" in data:
        if "position" in data:
            object = connectToMongo.createNewSectionInPosition(data.get("id"), data.get("section_name"),
                                                               data.get("position"))
        else:
            object = connectToMongo.createNewSection(data.get("id"), data.get("section_name"))
        return jsonify(response=200, agenda=object.makeJson())
    else:
        return jsonify(respose=400, msg="you didn't sent all the necessary information")


app.run()
