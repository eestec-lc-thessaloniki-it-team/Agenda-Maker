import re
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
        if type(database) is not str:
            raise TypeError('database must be of type string')
        url = """mongodb://{}:{}@116.203.85.249/{}""".format(mongo.user.username, mongo.user.password, database)
        self.client = MongoClient(url, authSource="admin")[database]
        self.db = self.client.lcThessaloniki
        # ping database to see if connection exists

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
        if type(json_agenda) is not dict:
            raise TypeError('json_agenda must be of type dict')
        if 'date' not in json_agenda:
            raise ValueError('json_agenda doesnt contain date field')
        if 'lc' not in json_agenda:
            raise ValueError('json_agenda doesnt contain lc field')

        if 'sections' not in json_agenda:
            raise ValueError('json_agenda doesnt contain sections field')

        if type(json_agenda['date']) is not str:
            raise TypeError('date must be of type str')
        if not bool(
                re.search("^([1-9]|0?[1-9]|1[0-9]| 2[0-9]|3[0-1])(/|.|-|)([1-9]|0?[1-9]|1[0-2])(/|.|-|)20[0-9][0-9]$",
                          json_agenda['date'])):  # TODO: it is not working for days 23-03-2020
            raise ValueError('date must be of format dd/mm/yyyy')
        if type(json_agenda['lc']) is not str:
            raise TypeError('lc must be of type str')

        if type(json_agenda['sections']) is not list:
            raise TypeError('sections must be of type dict')

        try:
            objectAgenda = Agenda(json_agenda.get("date"), json_agenda.get("lc"))
            agenda_id = str(self.db.agendas.insert_one(objectAgenda.makeJson()).inserted_id)
            object = Agenda(json_agenda.get("date"), json_agenda.get("lc"), agenda_id)
            return ResponseWrapper(object, found=True, operationDone=True)
        except:
            return ResponseWrapper(None)

    def getAgendaById(self, agenda_id) -> ResponseWrapper:
        """
        Returns an agenda based on requested id
        :param agenda_id:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        try:
            jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
            if jsonReturned is None:
                return ResponseWrapper(None)
            object = getAgendaFromJson(jsonReturned)
            object.id = agenda_id
            return ResponseWrapper(object, found=True, operationDone=True)
        except:
            return ResponseWrapper(None)

    def updateAgenda(self, agenda_id, new_agenda) -> Optional[ResponseWrapper]:
        """
        Replaces an agenda with agenda_id, with new_agenda
        :param agenda_id:
        :param new_agenda:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(new_agenda) is not dict:
            raise TypeError('new_agenda must be of type dict')
        if 'date' not in new_agenda:
            raise ValueError('new_agenda doesnt contain date field')
        if 'lc' not in new_agenda:
            raise ValueError('new_agenda doesnt contain lc field')
        if 'sections' not in new_agenda:
            raise ValueError('new_agenda doesnt contain sections field')
        if type(new_agenda['date']) is not str:
            raise TypeError('date must be of type str')
        if not bool(
                re.search("^([1-9]|0?[1-9]|1[0-9]| 2[0-9]|3[0-1])(/|.|-|)([1-9]|0?[1-9]|1[0-2])(/|.|-|)20[0-9][0-9]$",
                          new_agenda['date'])):  # TODO: move it as variable in the beginning and change message
            raise ValueError('date must be of format dd/mm/yyyy')
        if type(new_agenda['lc']) is not str:
            raise TypeError('lc must be of type str')
        if type(new_agenda['sections']) is not list:
            raise TypeError('sections must be of type dict')
        try:
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})
            return ResponseWrapper(self.getAgendaById(agenda_id).object, found=True,
                                   operationDone=bool(returned.matched_count))
        except:
            return ResponseWrapper(None)

    def updateSection(self, agenda_id, section_position, section_json) -> Optional[ResponseWrapper]:
        """
        Replaces a section in an existing agenda with agenda_id, with section_json
        :param agenda_id:
        :param section_position:
        :param section_json:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_position) is not int:
            raise TypeError('section_position must be of type int')
        if type(section_json) is not dict:
            raise TypeError('section_json must be of type dict')
        if 'section_name' not in section_json:
            raise ValueError('section_json doesnt contain sections field')
        if type(section_json['section_name']) is not str:
            raise TypeError('section_name must be of type str')
        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            objectAgenda.setSection(section_position, getSectionFromJson(section_json))
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count))
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def updateTopic(self, agenda_id, section_position, topic_position, topic_json) -> Optional[ResponseWrapper]:
        """
        Replaces a topic in an existing agenda with agenda_id, with topic_json
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_position) is not int:
            raise TypeError('section_position must be of type int')
        if type(topic_position) is not int:
            raise TypeError('topic_position must be of type int')
        if type(topic_json) is not dict:
            raise TypeError('topic_json must be of type dict')
        if 'topic_name' not in topic_json:
            raise ValueError('topic_json does not contain topic_name field')
        if 'votable' not in topic_json:
            raise ValueError('topic_json does not contain votable field')
        if type(topic_json["votable"]) is not bool:
            raise TypeError('votable must be of type bool')
        if topic_json['votable'] is True:
            if ('yes_no_vote' or 'open_ballot') not in topic_json:
                raise ValueError('topic_json doesnt contain yes_no_vote or open_ballot field')
            else:
                if topic_json['yes_no_vote'] is True:
                    if 'possible_answers' in topic_json:
                        raise ValueError('It is a YES/NO Vote, do not insert possible_answers field')
                elif topic_json['yes_no_vote'] is False:
                    if 'possible_answers' not in topic_json:
                        raise ValueError('topic_json does not contain possible_answers')
                else:
                    raise TypeError('yes_no_vote must be of type bool')
            if type(topic_json['open_ballot']) is not bool:
                raise TypeError('open_ballot must be of type bool')
        else:
            if ('yes_no_vote' or 'possible_answers' or 'open_ballot') in topic_json:
                raise ValueError(
                    'It is not a votable topic, do not insert yes_no_vote, possible_answers and open_ballot fields')

        try:
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
        except:
            return ResponseWrapper(None)

    def createNewSection(self, agenda_id, section_name):
        """
        Adds new session to existing agenda
        :param agenda_id:
        :param section_name:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_name) is not str:
            raise TypeError('section_name must be of type str')
        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            addedSection = objectAgenda.addSection(section_name)
            if not addedSection: return ResponseWrapper(objectAgenda, found=False, operationDone=False)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count))
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def createNewSectionInPosition(self, agenda_id, section_name, position):
        """
        Adds new session to existing agenda in requested position
        :param agenda_id:
        :param section_name:
        :param position:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_name) is not str:
            raise TypeError('section_name must be of type str')
        if type(position) is not int:
            raise TypeError('position must be of type int')
        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            objectAgenda.addSectionInPosition(section_name, position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count))
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def createNewTopic(self, agenda_id, section_position, topic_position, topic_json):
        """
        Adds a new topic to existing agenda in requested position
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_position) is not int:
            raise TypeError('section_position must be of type int')
        if type(topic_position) is not int:
            raise TypeError('topic_position must be of type int')
        if type(topic_json) is not dict:
            raise TypeError('topic_json must be of type dict')
        if 'topic_name' not in topic_json:
            raise ValueError('topic_json does not contain topic_name field')
        if 'votable' not in topic_json:
            raise ValueError('topic_json does not contain votable field')
        if type(topic_json["votable"]) is not bool:
            raise TypeError('votable must be of type bool')
        if topic_json['votable'] is True:
            if ('yes_no_vote' or 'open_ballot') not in topic_json:
                raise ValueError('topic_json doesnt contain yes_no_vote or open_ballot field')
            else:
                if topic_json['yes_no_vote'] is True:
                    if 'possible_answers' in topic_json:
                        raise ValueError('It is a YES/NO Vote, do not insert possible_answers field')
                elif topic_json['yes_no_vote'] is False:
                    if 'possible_answers' not in topic_json:
                        raise ValueError('topic_json does not contain possible_answers')
                else:
                    raise TypeError('yes_no_vote must be of type bool')
            if 'open_ballot' not in topic_json:
                raise ValueError('topic_json does not contain open_ballot field')
            if type(topic_json['open_ballot']) is not bool:
                raise TypeError('open_ballot must be of type bool')
        else:
            if ('yes_no_vote' or 'possible_answers' or 'open_ballot') in topic_json:
                raise ValueError(
                    'It is not a votable topic, do not insert yes_no_vote, possible_answers and open_ballot fields')

        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            objectAgenda.addTopicInPosition(section_position, getTopicFromJson(topic_json), topic_position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count))
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def deleteAgenda(self, agenda_id):
        """
        Deletes an agenda with agenda_id from the database
        :param agenda_id:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        try:
            agendaWrapper = self.getAgendaById(agenda_id)
            returned = self.db.agendas.delete_many({'_id': ObjectId(agenda_id)})
            return ResponseWrapper(agendaWrapper.object, found=agendaWrapper.found,
                                   operationDone=bool(returned.deleted_count))
        except:
            return ResponseWrapper(None)

    def deleteSection(self, agenda_id, position):
        """
        Deletes a section from agenda
        :param agenda_id:
        :param position:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(position) is not int:
            raise TypeError('position must be of type int')
        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            done = objectAgenda.deleteSection(position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count) and done)
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def deleteTopic(self, agenda_id, section_position, topic_position):
        """
        Deletes a topic from agenda
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :return: ResponseWrapper
        """
        if type(agenda_id) is not str:
            raise TypeError('agenda_id must be of type str')
        if type(section_position) is not int:
            raise TypeError('section_position must be of type int')
        if type(topic_position) is not int:
            raise TypeError('topic_position must be of type int')
        try:
            objectAgenda = self.getAgendaById(agenda_id).object
            done = objectAgenda.deleteTopic(section_position, topic_position)
            returned = self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': objectAgenda.makeJson()})
            responseWrapper: ResponseWrapper = ResponseWrapper(objectAgenda, found=True,
                                                               operationDone=bool(returned.matched_count) and done)
            return responseWrapper
        except:
            return ResponseWrapper(None)

    def deleteAll(self):
        """
        Deletes all agendas from the database
        :return: empty list
        """
        return self.db.agendas.drop()

# DON'T TOUCH OUR STAFF HERE!!
#
# mongo = connectMongo()
# a = mongo.createNewAgenda({"date": '09/05/2020', "lc": "LcThessaloniki", "sections": []})
# mongo.createNewSection(a.object.id,'tr')
# mongo.createNewTopic(a.object.id,0,0,{"topic_name": "openGmStaffEl", "votable": "False", 'yes_no_vote': False,"open_ballot": True})
#
# print(mongo.getAllAgendas())
#
# date="03-01-2017"
# print(bool(re.search("^([1-9]|0?[1-9]|1[0-9]| 2[0-9]|3[0-1])(/|.|-|)([1-9]|0?[1-9]|1[0-2])(/|.|-|)20[0-9][0-9]$",date)))
