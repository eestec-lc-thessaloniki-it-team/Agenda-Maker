import flask, os
from flask import request, jsonify
from mongo.connectMongo import *
from BasicClasses.Agenda import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
connectMongo = connectMongo()  # connection to mongo
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
    data = request.json
    if "date" in data and "lc" in data:
        responseWrapper: ResponseWrapper = connectMongo.createNewAgenda(request.json)
        return jsonify(response=200, agenda=responseWrapper.object.makeJson())
    else:
        return jsonify(response=400, msg="you didn't sent all the necessary information")


@app.route("/get-agenda-id", methods=['GET'])
def getAgendaByID():
    """
    In request I expect a string of ID
    :return: a object agenda as json + response
    """
    objectAgenda = getAgendaFromJson(connectMongo.getAgendaById(request.json.get("id")))
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
            responseWrapper: ResponseWrapper = connectMongo.createNewSectionInPosition(data.get("id"),
                                                                                       data.get("section_name"),
                                                                                       data.get("position"))
        else:
            responseWrapper: ResponseWrapper = connectMongo.createNewSection(data.get("id"), data.get("section_name"))
        return jsonify(response=200, agenda=responseWrapper.object.makeJson())
    else:
        return jsonify(respose=400, msg="you didn't sent all the necessary information")


@app.route("/create-topic", methods=['POST'])
def createTopic():
    """
    In request I expect agenda_id, section_position, topic_position, topic_json
    :return:
    """
    data = request.json
    if "id" in data and "section_position" in data and "topic_position" in data and "topic_json" in data:
        responseWrapper: ResponseWrapper = connectMongo.createNewTopic(data.get("id"), data.get("section_position"),
                                                                       data.get("topic_position"),
                                                                       data.get("topic_json"))
        return jsonify(response=200, agenda=responseWrapper.object.makeJson())
    else:
        return jsonify(respose=400, msg="you didn't sent all the necessary information")


@app.route("/update-agenda", methods=['POST'])
def updateAgenda():
    """
    In request I expect agenda_id, new_agenda
    :return:
    """
    data = request.json
    if "id" in data and "new_agenda" in data:
        responseWrapper: ResponseWrapper = connectMongo.updateAgenda(data.get("id"), data.get("new_agenda"))
        if not responseWrapper.found:
            return jsonify(response=404, msg="Agenda not found")
        return jsonify(response=200, agenda=responseWrapper.object.makeJson())
    else:
        return jsonify(respose=400, msg="you didn't sent all the necessary information")


@app.route("/delete-agenda", methods=['POST'])
def deleteAgenda():
    """
    In request I expect agenda_id
    :return:
    """
    data = request.json
    if "id" in data:
        connectMongo.deleteAgenda(data.get("id"))
        return jsonify(response=200, msg="Agenda has been deleted")
    else:
        return jsonify(respose=400, msg="you didn't sent all the necessary information")


if __name__ == '__main__':
    app.run()
