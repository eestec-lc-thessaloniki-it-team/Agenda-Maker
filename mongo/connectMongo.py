from bson import ObjectId
from pymongo import MongoClient
from datetime import date
from BasicClasses.Agenda import *
from BasicClasses.ResponseWrapper import ResponseWrapper
import mongo.user



database = "lcThessaloniki"
url = """mongodb://{}:{}@116.203.85.249/{}""".format(mongo.user.username, mongo.user.password, database)

def print_agenda(agenda):
    """
    Prints requested agenda
    :param agenda:
    """
    print(agenda.date, agenda.id, agenda.lc, agenda.sections)

def print_Wrapper(responseWrapper):
    print(responseWrapper.object,responseWrapper.found,responseWrapper.operationDone)

class connectMongo:

    def __init__(self):
        """
        Connection to database with credentials and get an object of mongoclient
        """
        self.client = MongoClient(url, authSource="admin")['lcThessaloniki']
        self.db = self.client.lcThessaloniki

    def getAllDatabasesFromLC(self):
        """
        Returns all databases from this LC
        :return: database
        """
        return self.client.list_collection_names()

    def getAllAgendas(self):
        """
        Returns all agendas from this database
        :return: List of all Agenda Objects
        """

        return [getAgendaFromJson(agendaJson) for agendaJson in self.db.agendas.find()]

    def createNewAgenda(self, json_agenda) -> ResponseWrapper:
        """
        Adds a new agenda to database
        :param json_agenda
        :return: ResponseWrapper
        """
        objectAgenda = Agenda(json_agenda.get("date"), json_agenda.get("lc"))
        id = self.db.agendas.insert_one(objectAgenda.makeJson()).inserted_id
        object = Agenda(json_agenda.get("date"), json_agenda.get("lc"), str(id))
        return ResponseWrapper(object,found=True,operationDone=True)

    def getAgendaJsonById(self, agenda_id):
        """
        Returns an agenda json based on requested id
        :param agenda_id:
        :return: Agenda json with agenda_id
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        return jsonReturned

    def getAgendaById(self, agenda_id) -> ResponseWrapper:
        """
        Returns an agenda based on requested id
        :param agenda_id:
        :return: agenda with agenda_id
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            return ResponseWrapper(None)
        object = getAgendaFromJson(jsonReturned)
        return ResponseWrapper(object,found=True,operationDone=True)


    def updateAgenda(self, agenda_id, new_agenda) -> Optional[ResponseWrapper]:
        """
        Replaces an agenda with agenda_id, with new_agenda
        :param agenda_id:
        :param new_agenda:
        :return: ResponseWrapper
        """
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})
        return ResponseWrapper(self.getAgendaById(agenda_id).object, found=True, operationDone=bool(returned.matched_count))

    def createNewSection(self, agenda_id, section_name):
        """
        Adds new session to existing agenda
        :param agenda_id:
        :param section_name:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            responseWrapper: ResponseWrapper = ResponseWrapper(None, found=False, operationDone=False)
        else:
            objectAgenda = getAgendaFromJson(jsonReturned)
            objectAgenda.addSection(section_name)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(self.getAgendaById(agenda_id).object, found=True, operationDone=bool(returned.matched_count))
        return responseWrapper

    def createNewSectionInPosition(self, agenda_id, section_name, position):
        """
        Adds new session to existing agenda in requested position
        :param agenda_id:
        :param section_name:
        :param position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            responseWrapper: ResponseWrapper = ResponseWrapper(None,found=False,operationDone=False)
        else:
            objectAgenda = getAgendaFromJson(jsonReturned)
            objectAgenda.addSectionInPosition(section_name, position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(self.getAgendaById(agenda_id).object,found=True,operationDone=bool(returned.matched_count))
        return responseWrapper

    def createNewTopic(self, agenda_id, section_position, topic_position, topic_json):
        """
        Adds a new topic to existing agenda in requested position
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            responseWrapper: ResponseWrapper = ResponseWrapper(None,found=False,operationDone=False)
        else:
            objectAgenda = getAgendaFromJson(jsonReturned)
            topic = getTopicFromJson(topic_json)
            objectAgenda.addTopicInPosition(section_position, topic, topic_position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(self.getAgendaById(agenda_id).object,found=True,operationDone=bool(returned.matched_count))
        return responseWrapper

    def deleteAgenda(self, agenda_id):
        """
        Deletes an agenda with agenda_id from the database
        :param agenda_id:
        :return: agenda object
        """
        agendaWrapper = self.getAgendaById(agenda_id)
        returned = self.db.agendas.delete_many({'id': agenda_id})
        return ResponseWrapper(agendaWrapper.object,found=agendaWrapper.found,operationDone=bool(returned.deleted_count))

    def deleteSection(self, agenda_id, position):
        """
        Deletes a section from agenda
        :param agenda_id:
        :param position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            responseWrapper: ResponseWrapper = ResponseWrapper(None,found=False, operationDone=False)
        else:
            objectAgenda = getAgendaFromJson(jsonReturned)
            objectAgenda.deleteSection(position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(self.getAgendaById(agenda_id).object,found=True,operationDone=bool(returned.matched_count))
        return responseWrapper

    def deleteTopic(self, agenda_id, section_position, topic_position):
        """
        Deletes a topic from agenda
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            responseWrapper: ResponseWrapper = ResponseWrapper(None,found=False,operationDone=False)
        else:
            objectAgenda = getAgendaFromJson(jsonReturned)
            objectAgenda.deleteTopic(section_position, topic_position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(self.getAgendaById(agenda_id).object,found=True,operationDone=bool(returned.matched_count))
        return responseWrapper

    def deleteAll(self):
        """
        Deletes all agendas from the database
        :return: empty list
        """
        return self.db.agendas.drop()


data = {
    "date": date.today().strftime("%d/%m/%Y"),
    "lc": "thessaloniki",
    "sections": [
        {
            "section_name": "gmElections",
            "topics": [
                {
                    "topic_name": "openGmstaffEl",
                    "votable": "True",
                    "yes_no_vote": "True",
                    "open_ballot": "False"
                },
                {
                    "topic_name": "MinutesElection",
                    "votable": "True",
                    "yes_no_vote": "False",
                    "possible_answers": ["Marios", "Tasos", "urMOM"],
                    "open_ballot": "True"
                }
            ]
        },
        {
            "section_name": "WorkShop",
            "topics": [
                {
                    "topic_name": "openVote",
                    "votable": "True",
                    "yes_no_vote": "True",
                    "open_ballot": "False"
                },
                {
                    "topic_name": "Future of Workshop",
                    "votable": "True",
                    "yes_no_vote": "False",
                    "possible_answers": ["Cancelation", "Postpone", "procced"],
                    "open_ballot": "True"
                }
            ]
        },
        {
            "section_name": "Krasia",
            "topics": [
                {
                    "topic_name": "openVote",
                    "votable": "True",
                    "yes_no_vote": "True",
                    "open_ballot": "False"
                },
                {
                    "topic_name": "Wanna go ?",
                    "votable": "True",
                    "yes_no_vote": "True",
                    "open_ballot": "True"
                },
                {
                    "topic_name": "Where",
                    "votable": "True",
                    "yes_no_vote": "False",
                    "possible_answers": ["Ombrella, Podhlato, SomeWeirdAssPlace"],
                    "open_ballot": "True"
                },
                {
                    "topic_name": "Lets go",
                    "votable": "False"
                }
            ]
        }
    ]
}



mongo = connectMongo()
a= mongo.createNewAgenda(data)
print(a.object)
print_agenda(a.object)
print_Wrapper(a)

mongo.updateAgenda(a.object.id,data)

b = mongo.createNewSectionInPosition(a.object.id,'mpur',0)
print_agenda(b.object)
print_Wrapper(b)

d = mongo.createNewTopic(a.object.id,0,0,{"topic_name": "Lets","votable": "False"})
print(mongo.getAgendaJsonById(d.object.id))
print_agenda(d.object)
print_Wrapper(d)

g = mongo.deleteTopic(a.object.id,0,0)
print(mongo.getAgendaJsonById(g.object.id))
print_Wrapper(g)

f = mongo.deleteSection(a.object.id,0)
print(mongo.getAgendaJsonById(f.object.id))
print_Wrapper(f)

print(mongo.getAllAgendas())