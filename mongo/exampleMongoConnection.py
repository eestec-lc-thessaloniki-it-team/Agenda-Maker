from bson import ObjectId
from pymongo import MongoClient
from datetime import date
from BasicClasses.Agenda import *

username = "root"
passwrod = "rootPassword"
database = "lcThessaloniki"

url = """mongodb://{}:{}@116.203.85.249/{}""".format(username, passwrod, database)

data2 = {'id': '1', 'date': '23-3-20', 'sections': [{'section_name': 'gmElections', 'topics': [
    {'topic_name': 'openGmstaffEl', 'votable': True, 'yes_no_vote': True, 'open_ballot': False},
    {'topic_name': 'MinutesElection', 'votable': True, 'yes_no_vote': False,
     'possible_answers': ['Marios', 'Tasos', 'urMOM'], 'open_ballot': True}]}, {'section_name': 'WorkShop', 'topics': [
    {'topic_name': 'openVote', 'votable': True, 'yes_no_vote': True, 'open_ballot': False},
    {'topic_name': 'Future of Workshop', 'votable': True, 'yes_no_vote': False,
     'possible_answers': ['Cancelation', 'Postpone', 'procced'], 'open_ballot': True}]}, {'section_name': 'Krasia',
                                                                                          'topics': [
                                                                                              {'topic_name': 'openVote',
                                                                                               'votable': True,
                                                                                               'yes_no_vote': True,
                                                                                               'open_ballot': False}, {
                                                                                                  'topic_name': 'Wanna go ?',
                                                                                                  'votable': True,
                                                                                                  'yes_no_vote': True,
                                                                                                  'open_ballot': True},
                                                                                              {'topic_name': 'Where',
                                                                                               'votable': True,
                                                                                               'yes_no_vote': False,
                                                                                               'possible_answers': [
                                                                                                   'Omprella, Podhlato, SomeWeirdAssPlace'],
                                                                                               'open_ballot': True},
                                                                                              {'topic_name': 'Lets go',
                                                                                               'votable': False}]}]}
data = {
    'id': '2',
    'lc': 'thessaloniki',
    'date': date.today().strftime("%d/%m/%Y"),
    'agenda': [  # this will be a list of objects  but for now lets assume that there are title, subtitle
        {
            'title': 'this is the first topic',
            'subtitle': 'this is its subtitle1'
        },
        {
            'title': 'this is the second topic',
            'subtitle': 'this is its subtitle2'
        }
    ]
}

newdata = {
    'id': '3',
    'lc': 'thessaloniki',
    'date': date.today().strftime("%d/%m/%Y"),
    'agenda': [  # this will be a list of objects  but for now lets assume that there are title, subtitle
        {
            'title': 'this is the first topic',
            'subtitle': 'this is its subtitle1'
        }
    ]
}


class connectMongo:

    def __init__(self):
        """
        connect to database with creadentials and get an object of mongoclient
        """
        self.client = MongoClient(url, authSource="admin")['lcThessaloniki']
        self.db = self.client.lcThessaloniki

    def getAllDatabasesFromLC(self):
        """
        :return: all the databases from this lc
        """
        return self.client.list_collection_names()

    def createNewAgenda(self, json_agenda):
        """
        Add this agenda to mongo
        :param json_agenda:
        :return:
        """
        objectAgenda = Agenda(json_agenda.get("date"), json_agenda.get("lc"))
        id = self.db.agendas.insert_one(objectAgenda.makeJson()).inserted_id
        object = Agenda(json_agenda.get("date"), json_agenda.get("lc"), str(id))
        return object

    def getAgendaById(self, agenda_id):
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        return jsonReturned

    def updateAgenda(self, agenda_id, new_agenda):
        return self.db.agendas.update_one({'id': agenda_id}, {'$set': new_agenda})

    def createNewTopic(self, agenda_id, section_position, topic_position, topic_json):
        """
        Get agenda
        Make it object
        Add topic
        Update agenda
        :param agenda_id:
        :param topic_json:
        :return:
        """
        pass

    def createNewSession(self, agenda_id, session_name):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param session_name:
        :return:
        """
        x = self.getAgendaById(agenda_id)
        return self.db.agendas.insert_one(session_name)

    def deleteNewTopic(self, agenda_id, topic_name):
        """
        Get agenda
        Make it object
        Add topic
        Update agenda
        :param agenda_id:
        :param topic_json:
        :return:
        """
        return self.db.agendas.delete_one({'id': agenda_id})

    def deleteNewSession(self, agenda_id, session_name):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param session_name:
        :return:
        """
        pass

    def deleteAgenda(self, agenda_id):
        return self.db.agendas.delete_many({'id': agenda_id})

# mongo = connectMongo()
#
# mongo.createNewAgenda(data)
# print(mongo.getAgendaById('2'))
#
# print(mongo.getAllDatabasesFromLC())
