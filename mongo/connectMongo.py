from bson import ObjectId
from pymongo import MongoClient
from datetime import date
from BasicClasses.Agenda import *
from BasicClasses.ResponseWrapper import ResponseWrapper
import mongo.user


class connectMongo:

    def __init__(self, database="lcThessaloniki"):
        """
        Connection to database with credentials and get an object of mongoclient
        """
        url = """mongodb://{}:{}@116.203.85.249/{}""".format(mongo.user.username, mongo.user.password, database)
        self.client = MongoClient(url, authSource="admin")[database]
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
        return ResponseWrapper(object, found=True,
                               operationDone=True)  # TODO: try except statement if everything went ok

    def getAgendaById(self, agenda_id) -> ResponseWrapper:
        """
        Returns an agenda based on requested id
        :param agenda_id:
        :return: ResponseWrapper
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        if jsonReturned is None:
            return ResponseWrapper(None)
        object = getAgendaFromJson(jsonReturned)
        object.id = agenda_id
        return ResponseWrapper(object, found=True, operationDone=True)

    def updateAgenda(self, agenda_id, new_agenda) -> Optional[ResponseWrapper]:
        """
        Replaces an agenda with agenda_id, with new_agenda
        :param agenda_id:
        :param new_agenda:
        :return: ResponseWrapper
        """
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})
        return ResponseWrapper(self.getAgendaById(agenda_id).object, found=True,
                               operationDone=bool(returned.matched_count))

    def updateSection(self, agenda_id, section_position, section_json) -> Optional[ResponseWrapper]:
        """
        Replaces a section in an existing agenda with agenda_id, with section_json
        :param agenda_id:
        :param section_position:
        :param section_json:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        objectAgenda.setSection(section_position, getSectionFromJson(section_json))
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count))
        return responseWrapper

    def updateTopic(self, agenda_id, section_position, topic_position, topic_json) -> Optional[ResponseWrapper]:
        """
        Replaces a topic in an existing agenda with agenda_id, with topic_json
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        done = objectAgenda.setTopic(section_position, topic_position, getTopicFromJson(topic_json))
        if done:
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            operationDone = bool(returned.matched_count)
        else:
            operationDone = False
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=operationDone)
        return responseWrapper

    def createNewSection(self, agenda_id, section_name):
        """
        Adds new session to existing agenda
        :param agenda_id:
        :param section_name:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        addedSection = objectAgenda.addSection(section_name)
        if not addedSection: return ResponseWrapper(objectAgenda, found=False, operationDone=False)
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count))
        return responseWrapper

    def createNewSectionInPosition(self, agenda_id, section_name, position):
        """
        Adds new session to existing agenda in requested position
        :param agenda_id:
        :param section_name:
        :param position:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        objectAgenda.addSectionInPosition(section_name, position)
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count))
        return responseWrapper

    def createNewTopic(self, agenda_id, section_position, topic_position, topic_json):
        """
        Adds a new topic to existing agenda in requested position
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        objectAgenda.addTopicInPosition(section_position, getTopicFromJson(topic_json), topic_position)
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count))
        return responseWrapper

    def deleteAgenda(self, agenda_id):
        """
        Deletes an agenda with agenda_id from the database
        :param agenda_id:
        :return: ResponseWrapper
        """
        agendaWrapper = self.getAgendaById(agenda_id)
        returned = self.db.agendas.delete_many({'id': agenda_id})
        return ResponseWrapper(agendaWrapper.object, found=agendaWrapper.found,
                               operationDone=bool(returned.deleted_count))

    def deleteSection(self, agenda_id, position):
        """
        Deletes a section from agenda
        :param agenda_id:
        :param position:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        done = objectAgenda.deleteSection(position)
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count) and done)
        return responseWrapper

    def deleteTopic(self, agenda_id, section_position, topic_position):
        """
        Deletes a topic from agenda
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :return: ResponseWrapper
        """
        objectAgenda = self.getAgendaById(agenda_id).object
        done = objectAgenda.deleteTopic(section_position, topic_position)
        returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
        responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                           operationDone=bool(returned.matched_count) and done)
        return responseWrapper

    def deleteAll(self):
        """
        Deletes all agendas from the database
        :return: empty list
        """
        return self.db.agendas.drop()


'''
mongo = connectMongo()
print(mongo.getAllDatabasesFromLC())
'''
