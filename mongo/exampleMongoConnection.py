from bson import ObjectId
from pymongo import MongoClient
from datetime import date
from BasicClasses.Agenda import *
import mongo.user

database = "lcThessaloniki"

url = """mongodb://{}:{}@116.203.85.249/{}""".format(mongo.user.username, mongo.user.password, database)

### Egw toy eipa na ta svisoume ta data!!!
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
    """"""
    sections = []
    jsonSection = list(agenda_json.get("sections"))
    for sec in jsonSection:
        jsonTopics = list(sec.get("topics"))
        topics = []

        for jsontopic in jsonTopics:
            topic = getTopicFromJson(jsontopic)
            topics.append(topic)
        section = Section(sec.get("section_name"), topics)
        sections.append(section)
    object = Agenda(agenda_json.get("date"), agenda_json.get("lc"), agenda_id, sections)
    return object


class connectMongo:

    def __init__(self):
        """
        connect to database with credentials and get an object of mongoclient
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
        :return: a cursor to all agendas
        """
        return self.db.agendas.find()

    def createNewAgenda(self, json_agenda):
        """
        adds a new agenda to database
        :param json_agenda
        :return: added agenda object
        """
        objectAgenda = Agenda(json_agenda.get("date"), json_agenda.get("lc"))
        id = self.db.agendas.insert_one(objectAgenda.makeJson()).inserted_id
        object = Agenda(json_agenda.get("date"), json_agenda.get("lc"), str(id))
        return object

    def getAgendaJsonById(self, agenda_id):
        """
        Returns an agenda json based on requested id
        :param agenda_id:
        :return: agenda json with agenda_id
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        return jsonReturned

    def getAgendaById(self, agenda_id):
        """
        Returns an agenda based on requested id
        :param agenda_id:
        :return: agenda with agenda_id
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = Agenda(jsonReturned.get("date"), jsonReturned.get("lc"), str(agenda_id), jsonReturned.get("sections"))
        return object

    def updateAgenda(self, agenda_id, new_agenda):
        """
        Replaces an agenda with agenda_id, with new_agenda
        :param agenda_id:
        :param new_agenda:
        :return:
        """
        return self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': new_agenda})

    def createNewSection(self, agenda_id, section_name):
        """
        Adds new session to existing agenda
        :param agenda_id:
        :param section_name:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
        #object = getAgendaFromJson(jsonReturned)
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
        # object = getAgendaFromJson(jsonReturned)
        object = agendaJsonToAgendaObject(jsonReturned,agenda_id)
        object.addSectionInPosition(section_name, position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def createNewTopic(self, agenda_id, section_position, topic_position, topic_json):
        """
        Adds new topic to existing agenda in requested position
        :param agenda_id:
        :param section_position:
        :param topic_position:
        :param topic_json:
        :return: agenda object
        """
        jsonReturned = self.db.agendas.find_one({'_id': ObjectId(agenda_id)})
        # object = getAgendaFromJson(jsonReturned)
        object= agendaJsonToAgendaObject(jsonReturned, agenda_id)
        topic = getTopicFromJson(topic_json)
        object.addTopicInPosition(section_position, topic, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object

    def deleteAgenda(self, agenda_id):
        """
        Deletes an agenda with agenda_id
        :param agenda_id:
        :return:
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
        # object = getAgendaFromJson(jsonReturned)
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
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
        # object = getAgendaFromJson(jsonReturned)
        object = agendaJsonToAgendaObject(jsonReturned, agenda_id)
        object.deleteTopic(section_position, topic_position)
        self.db.agendas.update_one({'_id': ObjectId(agenda_id)}, {'$set': object.makeJson()})
        return object


    def deleteAll(self):
        """
        Deletes all agendas from database
        :return:
        """
        return self.db.agendas.drop()


def print_agenda(agenda):
    print(agenda.date, agenda.id, agenda.lc, agenda.sections)

"""
mongo = connectMongo()

a = mongo.createNewAgenda(data)
print_agenda(a)


mongo.updateAgenda(a.id, data)
b = mongo.getAgendaById(a.id)
print_agenda(b)


mongo.createNewSectionInPosition(a.id, 'Krasiaaaaaa', 0)
b = mongo.getAgendaById(a.id)
print_agenda(b)

mongo.createNewTopic(b.id,0,0,{'topic_name': 'openGmstaffEl', 'votable': 'True', 'yes_no_vote': 'True', 'open_ballot': 'False'})
c = mongo.getAgendaById(b.id)
print_agenda(c)

mongo.deleteSection(a.id,1)
d=mongo.getAgendaById(a.id)
print_agenda(d)

mongo.deleteSection(a.id,0)
d = mongo.getAgendaObjectById(a.id)
print_agenda(d)

mongo.deleteTopic(a.id,0,0)
e = mongo.getAgendaObjectById(a.id)
print_agenda(e)

mongo.deleteAll()

s = mongo.getAllAgendas()
print(list(s))
"""