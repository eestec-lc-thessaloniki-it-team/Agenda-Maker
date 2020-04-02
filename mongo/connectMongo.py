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
    :return: Agenda
    """
    print(agenda.date, agenda.id, agenda.lc, agenda.sections)


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
        :return: a cursor to all agendas
        """
        return self.db.agendas.find()

    def createNewAgenda(self, json_agenda) -> ResponseWrapper:
        """
        Adds a new agenda to database
        :param json_agenda
        :return: added agenda object
        """
        objectAgenda = Agenda(json_agenda.get("date"), json_agenda.get("lc"))
        id = self.db.agendas.insert_one(objectAgenda.makeJson()).inserted_id
        object = Agenda(json_agenda.get("date"), json_agenda.get("lc"), str(id))
        return ResponseWrapper(object)

    def getAgendaJsonById(self, agenda_id):
        """
        Returns an agenda json based on requested id
        :param agenda_id:
        :return: agenda json with agenda_id
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
        # object = Agenda(jsonReturned.get("date"), jsonReturned.get("lc"), str(agenda_id), jsonReturned.get("sections"))
        object = getAgendaFromJson(jsonReturned)
        return ResponseWrapper(object)

    def updateAgenda(self, agenda_id, new_agenda) -> Optional[ResponseWrapper]:
        """
        Replaces an agenda with agenda_id, with new_agenda
        :param agenda_id:
        :param new_agenda:
        :return: agenda object
        """
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})
        if returned.matched_count:
            objectAgenda = self.getAgendaById(agenda_id).object
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True, operationDone=True)
            return responseWrapper
        else:
            responseWrapper: ResponseWrapper = ResponseWrapper(None, found=False, operationDone=False)
            return responseWrapper

    def createNewSection(self, agenda_id, section_name):
        """
        Adds new session to existing agenda
        :param agenda_id:
        :param section_name:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = getAgendaFromJson(jsonReturned)
        object.addSection(section_name)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def createNewSectionInPosition(self, agenda_id, section_name, position):
        """
        Adds new session to existing agenda in requested position
        :param agenda_id:
        :param section_name:
        :param position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = getAgendaFromJson(jsonReturned)
        object.addSectionInPosition(section_name, position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

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
        object = getAgendaFromJson(jsonReturned)
        topic = getTopicFromJson(topic_json)
        object.addTopicInPosition(section_position, topic, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteAgenda(self, agenda_id):
        """
        Deletes an agenda with agenda_id from the database
        :param agenda_id:
        :return: agenda object
        """
        return self.db.agendas.delete_many({'id': agenda_id})

    def deleteSection(self, agenda_id, position):
        """
        Deletes a section from agenda
        :param agenda_id:
        :param position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = getAgendaFromJson(jsonReturned)
        object.deleteSection(position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteTopic(self, agenda_id, section_position, topic_position):
        """
        Deletes a topic from agenda
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = getAgendaFromJson(jsonReturned)
        object.deleteTopic(section_position, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteAll(self):
        """
        Deletes all agendas from the database
        :return: empty list
        """
        return self.db.agendas.drop()
