import unittest
from mongo.connectMongo import *

"""
class MongoTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.json = {"date": date.today().strftime("%d/%m/%Y"), "lc": "thessaloniki","sections": [
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

    def test_getAgendaJsonById(self):
        self.assertDictEqual(mongo.getAgendaJsonById(self),self.mongo.makeJson())

    def test_getAgendaById(self):
        self.assertEqual(mongo.getAgendaById(self),self.agenda)

    def test_createAgenda(self):
        self.assertEqual()

    def test_updateAgenda(self):
        self.assertEqual()

    def test_createNewSection(self):
        self.assertEqual()

    def test_createNewSectionInPosition(self):
        self.assertEqual()

    def test_createNewTopic(self):
        self.assertEqual()

    def test_deleteAgenda(self):
        self.assertEqual()

    def test_deleteSection(self):
        self.assertEqual()

    def test_deleteTopic(self):
        self.assertEqual()
        
"""

# data2 = {
#     'date': date.today().strftime("%d/%m/%Y"),
#     'lc': 'thessaloniki',
#     'sections': [  # this will be a list of objects  but for now lets assume that there are title, subtitle
#         {
#             'section_name': 'Section 1',
#             'topics': []
#         },
#         {
#             'section_name': 'Section 2',
#             'topics': []
#         }
#     ]
# }

data = {"date": date.today().strftime("%d/%m/%Y"), "lc": "thessaloniki","sections": [
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


def print_agenda(agenda):
    """
    Prints requested agenda
    :param agenda:
    """
    print(agenda.date, agenda.id, agenda.lc, agenda.sections)

def print_Wrapper(responseWrapper):
    print(responseWrapper.object,responseWrapper.found,responseWrapper.operationDone)


mongo = connectMongo()

a = mongo.createNewAgenda(data)
print_agenda(a.object)
print_Wrapper(a)

a = mongo.updateAgenda(a.object.id, data)
print_agenda(a.object)
print_Wrapper(a)

b = mongo.getAgendaById(a.object.id)
print_agenda(b.object)
print_Wrapper(b)

c = mongo.createNewSectionInPosition(a.object.id, 'New Section!', 0)
print_agenda(c.object)
print_Wrapper(c)

d = mongo.deleteSection(a.object.id, 0)
print_agenda(d.object)
print_Wrapper(d)

e = mongo.createNewTopic(a.object.id, 0, 0, {'topic_name': 'New Topic!', 'votable': 'True', 'yes_no_vote': 'True', 'open_ballot': 'False'})
print_agenda(e.object)
print_Wrapper(e)

f = mongo.deleteTopic(a.object.id, 0, 0)
print(mongo.getAgendaById(f.object.id))
print_Wrapper(f)

g = mongo.deleteSection(a.object.id,0)
print(mongo.getAgendaById(g.object.id))
print_Wrapper(g)

print(mongo.getAllAgendas())