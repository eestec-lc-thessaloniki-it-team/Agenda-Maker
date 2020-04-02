from mongo.connectMongo import *

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

data2 = {
    'date': date.today().strftime("%d/%m/%Y"),
    'lc': 'thessaloniki',
    'sections': [  # this will be a list of objects  but for now lets assume that there are title, subtitle
        {
            'section_name': 'Section 1',
            'topics': []
        },
        {
            'section_name': 'Section 2',
            'topics': []
        }
    ]
}

"""
Auta ta xoume kai stin exampleMongoConnection, den xreiazontai edw, alla oti theleis!!
def print_agenda(agenda):
    print(agenda.date, agenda.id, agenda.lc, agenda.sections)

mongo = connectMongo()
"""
mongo = connectMongo()
a = mongo.createNewAgenda(data)
print_agenda(a)  # Prints the new agenda that was created

aa = mongo.createNewAgenda(data2)
s = mongo.getAllAgendas()
print(list(s))  # Prints a list of json agendas

mongo.updateAgenda(a.id, data)
b = mongo.getAgendaById(a.id)
print_agenda(b)  # Prints updated agenda

s = mongo.getAllAgendas()
print(list(s))  # Prints a list of json agendas

mongo.createNewSectionInPosition(a.id, 'Krasiaaaaaa', 0)
c = mongo.getAgendaById(a.id)
print_agenda(c)  # Prints agenda with new section

mongo.deleteSection(a.id, 0)
d = mongo.getAgendaById(a.id)
print_agenda(d)  # Prints agenda with deleted section

mongo.createNewTopic(a.id, 0, 0,
                     {'topic_name': 'Test', 'votable': 'True', 'yes_no_vote': 'True', 'open_ballot': 'False'})
e = mongo.getAgendaById(a.id)
print_agenda(e)  # Prints agenda with new topic

mongo.deleteTopic(a.id, 0, 0)
f = mongo.getAgendaById(a.id)
print_agenda(f)  # Prints agenda with deleted topic

mongo.deleteAll()  # Deletes all agendas
s = mongo.getAllAgendas()
print(list(s))
