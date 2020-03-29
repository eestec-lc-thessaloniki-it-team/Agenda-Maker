from bson import ObjectId
from pymongo import MongoClient
from datetime import date
from BasicClasses.Agenda import *

username = "root"
passwrod = ""
database = "lcThessaloniki"

url = """mongodb://{}:{}@116.203.85.249/{}""".format(username, passwrod, database)
data = {
    "id": "1",
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
                "possible_answers": ["Marios", "Tasos", "urMOM"
                    ],
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
                    "possible_answers": ["Omprella, Podhlato, SomeWeirdAssPlace"
                    ],
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
data2 = {
    'id': '2',
    'lc': 'thessaloniki',
    'date': date.today().strftime("%d/%m/%Y"),
    'sections': [  # this will be a list of objects  but for now lets assume that there are title, subtitle
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

def agendaJsonToAgendaObject(agenda_json, agenda_id):
    sections = []
    jsonSection = list(agenda_json.get("sections"))
    for sec in jsonSection:
        jsonTopics = list(sec.get("topics"))
        topics = []

        for jsontopic in jsonTopics:
            topic = Topic(jsontopic.get("topic_name"), jsontopic.get("votable"))
            topics.append(topic)
        section = Section(sec.get("section_name"), topics)
        sections.append(section)
    object = Agenda(agenda_json.get("date"), agenda_id, agenda_json.get("lc"), sections)
    return object

def topicJsonToTopicObject(topic_json):
    topic = Topic(topic_json.get("topic_name"), topic_json.get("votable"))
    return topic


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

    def getAllAgendas(self):
        """
        :return:
        :return:
        """
        return self.db.agendas.find()

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

    ### TO DO: Convert sections json to objects ###
    def getAgendaObjectById(self, agenda_id):
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = Agenda(jsonReturned.get("date"), jsonReturned.get("lc"), str(agenda_id), jsonReturned.get("sections"))
        return object

    def updateAgenda(self, agenda_id, new_agenda):
        return self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})

    def createNewSection(self, agenda_id, section_name):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param section_name:
        :return:
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
        object.addSection(section_name)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object


    def createNewSectionInPosition(self, agenda_id, section_name, position):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param section_name:
        :return:
        """

        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        sections = []
        jsonSection = list(jsonReturned.get("sections"))
        for sec in jsonSection:
            jsonTopics = list(sec.get("topics"))
            topics = []

            for jsontopic in jsonTopics:
                topic = Topic(jsontopic.get("topic_name"), jsontopic.get("votable"))
                topics.append(topic)
            section = Section(sec.get("section_name"), topics)
            sections.append(section)
        object = Agenda(jsonReturned.get("date"), agenda_id, jsonReturned.get("lc"), sections)
        object.addSectionInPosition(section_name, position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

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

        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object= agendaJsonToAgendaObject(jsonReturned, agenda_id)
        topic = topicJsonToTopicObject(topic_json)
        object.addTopicInPosition(section_position, topic, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteSection(self, agenda_id, position):
        """
        Get agenda
        Make it object
        Add session with name
        Update agenda
        :param agenda_id:
        :param session_name:
        :return:
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
        object.deleteSection(position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteTopic(self, agenda_id, section_position, topic_position):
        """
        Get agenda
        Make it object
        Add topic
        Update agenda
        :param agenda_id:
        :param topic_json:
        :return:
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
        object.deleteTopic(section_position, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteAgenda(self, agenda_id):
        return self.db.agendas.delete_many({'id': agenda_id})


def print_agenda(agenda):
    print(agenda.id, agenda.date, agenda.lc, agenda.sections)

mongo = connectMongo()

a = mongo.createNewAgenda(data)
print_agenda(a)

mongo.updateAgenda(a.id, data)
b = mongo.getAgendaObjectById(a.id)
print_agenda(b)

mongo.createNewSection(a.id, 'Krasiaaaaa')
mongo.createNewSectionInPosition(a.id, 'Krasiaaaaaa', 0)
b = mongo.getAgendaObjectById(a.id)
print_agenda(b)

mongo.createNewTopic(b.id,0,0,{'topic_name': 'openGmstaffEl', 'votable': 'True', 'yes_no_vote': 'True', 'open_ballot': 'False'})
c = mongo.getAgendaObjectById(b.id)
print_agenda(c)

mongo.deleteSection(a.id,0)
d = mongo.getAgendaObjectById(a.id)
print_agenda(d)

mongo.deleteTopic(a.id,0,0)
e = mongo.getAgendaObjectById(a.id)
print_agenda(e)

s = mongo.getAllAgendas()
print(list(s))
