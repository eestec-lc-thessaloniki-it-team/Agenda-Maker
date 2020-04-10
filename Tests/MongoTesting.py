import unittest
from mongo.connectMongo import *


class MongoTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.mongo = connectMongo()
        self.json = {"date": date.today().strftime("%d/%m/%Y"), "lc": "thessaloniki", "sections": [
            {
                "section_name": "gmElections",
                "topics": [
                    {
                        "topic_name": "openGmstaffEl",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    },
                    {
                        "topic_name": "MinutesElection",
                        "votable": True,
                        "yes_no_vote": False,
                        "possible_answers": ["Marios", "Tasos", "urMOM"],
                        "open_ballot": True
                    }
                ]
            },
            {
                "section_name": "WorkShop",
                "topics": [
                    {
                        "topic_name": "openVote",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    },
                    {
                        "topic_name": "Future of Workshop",
                        "votable": True,
                        "yes_no_vote": False,
                        "possible_answers": ["Cancelation", "Postpone", "procced"],
                        "open_ballot": True
                    }
                ]
            },
            {
                "section_name": "Krasia",
                "topics": [
                    {
                        "topic_name": "openVote",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    },
                    {
                        "topic_name": "Wanna go ?",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": True
                    },
                    {
                        "topic_name": "Where",
                        "votable": True,
                        "yes_no_vote": False,
                        "possible_answers": ["Ombrella, Podhlato, SomeWeirdAssPlace"],
                        "open_ballot": True
                    },
                    {
                        "topic_name": "Lets go",
                        "votable": False
                    }
                ]
            }
        ]
                     }

        self.testAgenda = {"date": "10/05/2020", "lc": "thessaloniki"}
        self.testAgenda2 = {"date": "11/05/2020", "lc": "Thessaloniki", "sections": [
            {
                "section_name": "Testing1",
                "topics": [
                    {
                        "topic_name": "Topic1",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    }]}]}
        self.topic = {
                        "topic_name": "TestTopicName",
                        "votable": True,
                        "yes_no_vote": False,
                        "open_ballot": False
                    }

    def test_getAllDatabasesFromLc(self):
        self.assertEqual(self.mongo.getAllDatabasesFromLC(), ['lcThessaloniki.agendas'])

    def test_getAgendaById(self):
        responseWrapper = self.mongo.createNewAgenda(self.testAgenda)
        wrapper = ResponseWrapper(responseWrapper.object, True, True)
        x = self.mongo.getAgendaById(responseWrapper.object.id)
        self.assertEqual(x.object, wrapper.object)
        self.assertTrue(x.found)
        self.assertTrue(x.operationDone)

    def test_createAgenda(self):
        responseWrapper = self.mongo.createNewAgenda(self.testAgenda)
        self.assertEqual(responseWrapper.object.date, "10/05/2020")
        self.assertEqual(responseWrapper.object.lc, "thessaloniki")
        self.assertEqual(responseWrapper.object.sections, [])
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)

    def test_updateAgenda(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda)
        responseWrapper = self.mongo.updateAgenda(createdResponseWrapper.object.id, self.testAgenda2)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, "Testing1")
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "Topic1")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)

    def test_createNewSection(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda2)
        self.mongo.updateAgenda(createdResponseWrapper.object.id,self.testAgenda2)
        responseWrapper = self.mongo.createNewSection(createdResponseWrapper.object.id, 'TestSectionName')
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, "Testing1")
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "Topic1")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[1].section_name, "TestSectionName")
        self.assertEqual(responseWrapper.object.sections[1].topics, [])


    def test_createNewSectionInPosition(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda2)
        self.mongo.updateAgenda(createdResponseWrapper.object.id,self.testAgenda2)
        responseWrapper = self.mongo.createNewSectionInPosition(createdResponseWrapper.object.id, 'TestSectionName',0)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, "TestSectionName")
        self.assertEqual(responseWrapper.object.sections[0].topics, [])
        self.assertEqual(responseWrapper.object.sections[1].section_name, "Testing1")
        self.assertEqual(responseWrapper.object.sections[1].topics[0].topic_name, "Topic1")
        self.assertTrue(responseWrapper.object.sections[1].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[1].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[1].topics[0].open_ballot)


    def test_createNewTopic(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda2)
        self.mongo.updateAgenda(createdResponseWrapper.object.id, self.testAgenda2)
        responseWrapper = self.mongo.createNewTopic(createdResponseWrapper.object.id, 0, 0, self.topic)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'Testing1')
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "TestTopicName")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].topic_name, "Topic1")
        self.assertTrue(responseWrapper.object.sections[0].topics[1].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[1].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[1].open_ballot)


    def test_deleteAgenda(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda)
        responseWrapper= self.mongo.deleteAgenda(createdResponseWrapper.object.id)
        self.assertEqual(responseWrapper.object,createdResponseWrapper.object)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        a = self.mongo.getAgendaById(responseWrapper.object.id)
        self.assertFalse(a.found)
        self.assertFalse(a.operationDone)


    def test_deleteSection(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda2)
        self.mongo.updateAgenda(createdResponseWrapper.object.id, self.testAgenda2)
        responseWrapper = self.mongo.deleteSection(createdResponseWrapper.object.id,0)
        self.assertEqual(responseWrapper.object.sections,[])
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")


    def test_deleteTopic(self):
        createdResponseWrapper = self.mongo.createNewAgenda(self.testAgenda2)
        self.mongo.updateAgenda(createdResponseWrapper.object.id, self.testAgenda2)
        responseWrapper = self.mongo.deleteTopic(createdResponseWrapper.object.id, 0,0)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'Testing1')
        self.assertEqual(responseWrapper.object.sections[0].topics, [])


if __name__ == '__main__':
    unittest.main()
