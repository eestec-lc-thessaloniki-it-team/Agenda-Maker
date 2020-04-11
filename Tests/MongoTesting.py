import unittest
from mongo.connectMongo import *


class MongoTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.mongo = connectMongo()

        self.testJson = {"date": '09/05/2020', "lc": "LcThessaloniki", "sections": [
            {
                "section_name": "gmElections",
                "topics": [
                    {
                        "topic_name": "openGmStaffEl",
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
                        "possible_answers": ["Cancellation", "Postpone", "Proceed"],
                        "open_ballot": True
                    }
                ]
            },
            {
                "section_name": "BEERs",
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
                        "possible_answers": ["Ombrella, Podhlato, RandomPlace"],
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

        self.testJson2 = {"date": "11/05/2020", "lc": "Thessaloniki", "sections": [
            {
                "section_name": "Testing1",
                "topics": [
                    {
                        "topic_name": "Topic1",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    }]}]}

        self.testJson3 = {"date": "10/05/2020", "lc": "thessaloniki"}

        self.topic = {
                        "topic_name": "TestTopicName",
                        "votable": True,
                        "yes_no_vote": True,
                        "open_ballot": False
                    }

        self.createdWrapper = self.mongo.createNewAgenda(self.testJson)




    def test_getAllDatabasesFromLc(self):
        self.assertEqual(self.mongo.getAllDatabasesFromLC(), ['lcThessaloniki.agendas'])

    def test_getAgendaById(self):
        """
        Tested all arguments of getAgendaById function
        """
        responseWrapper = self.mongo.getAgendaById(self.createdWrapper.object.id)
        self.assertEqual(responseWrapper.object, self.createdWrapper.object)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        responseWrapper = self.mongo.getAgendaById('123456789')
        self.assertIsNone(responseWrapper.object)
        self.assertFalse(responseWrapper.found)
        self.assertFalse(responseWrapper.operationDone)

    def test_createAgenda(self):
        """
        Tested all arguments of self.testJson3 after creating an agenda
        """
        self.assertEqual(self.createdWrapper.object.date, "09/05/2020")
        self.assertEqual(self.createdWrapper.object.lc, "LcThessaloniki")
        self.assertEqual(self.createdWrapper.object.sections, [])
        self.assertTrue(self.createdWrapper.found)
        self.assertTrue(self.createdWrapper.operationDone)

    def test_updateAgenda(self):
        """
        Tested all arguments of self.testJson2 after updating an agenda
        """
        responseWrapper = self.mongo.updateAgenda(self.createdWrapper.object.id, self.testJson2)
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
        """
        Tested all arguments of self.testJson2 after creating a section
        """
        self.mongo.updateAgenda(self.createdWrapper.object.id,self.testJson2)
        responseWrapper = self.mongo.createNewSection(self.createdWrapper.object.id, 'TestSectionName')
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
        """
        Tested all arguments of self.testJson2 after creating a section in position
        """
        self.mongo.updateAgenda(self.createdWrapper.object.id,self.testJson2)
        responseWrapper = self.mongo.createNewSectionInPosition(self.createdWrapper.object.id, 'TestSectionName',0)
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
        """
        Tested all arguments of self.testJson2 after creating a topic
        """
        self.mongo.updateAgenda(self.createdWrapper.object.id, self.testJson2)
        responseWrapper = self.mongo.createNewTopic(self.createdWrapper.object.id, 0, 0, self.topic)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "11/05/2020")
        self.assertEqual(responseWrapper.object.lc, "Thessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'Testing1')
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "TestTopicName")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].topic_name, "Topic1")
        self.assertTrue(responseWrapper.object.sections[0].topics[1].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[1].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[1].open_ballot)


    def test_deleteAgenda(self):
        """
        Tested all arguments of self.testJson after deleting an agenda
        """
        responseWrapper= self.mongo.deleteAgenda(self.createdWrapper.object.id)
        self.assertEqual(responseWrapper.object,self.createdWrapper.object)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        a = self.mongo.getAgendaById(responseWrapper.object.id)
        self.assertFalse(a.found)
        self.assertFalse(a.operationDone)


    def test_deleteSection(self):
        """
        Tested all arguments of self.testJson after deleting a section
        """
        self.mongo.updateAgenda(self.createdWrapper.object.id, self.testJson)
        responseWrapper = self.mongo.deleteSection(self.createdWrapper.object.id,2)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "09/05/2020")
        self.assertEqual(responseWrapper.object.lc, "LcThessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'gmElections')
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "openGmStaffEl")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].topic_name, "MinutesElection")
        self.assertTrue(responseWrapper.object.sections[0].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[0].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].possible_answers,["Marios", "Tasos", "urMOM"])
        self.assertTrue(responseWrapper.object.sections[0].topics[1].open_ballot)
        self.assertEqual(responseWrapper.object.sections[1].section_name, 'WorkShop')
        self.assertEqual(responseWrapper.object.sections[1].topics[0].topic_name, "openVote")
        self.assertTrue(responseWrapper.object.sections[1].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[1].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[1].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[1].topics[1].topic_name, "Future of Workshop")
        self.assertTrue(responseWrapper.object.sections[1].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[1].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[1].topics[1].possible_answers,["Cancellation", "Postpone", "Proceed"])
        self.assertTrue(responseWrapper.object.sections[1].topics[1].open_ballot)
        responseWrapper = self.mongo.deleteSection(self.createdWrapper.object.id, 0)
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'WorkShop')
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "openVote")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].topic_name, "Future of Workshop")
        self.assertTrue(responseWrapper.object.sections[0].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[0].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].possible_answers,["Cancellation", "Postpone", "Proceed"])
        self.assertTrue(responseWrapper.object.sections[0].topics[1].open_ballot)
        self.mongo.deleteSection(self.createdWrapper.object.id, 0)



    def test_deleteTopic(self):
        """
        Tested all arguments of self.testJson after deleting a topic
        """
        self.mongo.updateAgenda(self.createdWrapper.object.id, self.testJson)
        responseWrapper = self.mongo.deleteTopic(self.createdWrapper.object.id, 2,1)
        self.assertTrue(responseWrapper.found)
        self.assertTrue(responseWrapper.operationDone)
        self.assertEqual(responseWrapper.object.date, "09/05/2020")
        self.assertEqual(responseWrapper.object.lc, "LcThessaloniki")
        self.assertEqual(responseWrapper.object.sections[0].section_name, 'gmElections')
        self.assertEqual(responseWrapper.object.sections[0].topics[0].topic_name, "openGmStaffEl")
        self.assertTrue(responseWrapper.object.sections[0].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[0].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[0].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].topic_name, "MinutesElection")
        self.assertTrue(responseWrapper.object.sections[0].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[0].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[0].topics[1].possible_answers,["Marios", "Tasos", "urMOM"])
        self.assertTrue(responseWrapper.object.sections[0].topics[1].open_ballot)
        self.assertEqual(responseWrapper.object.sections[1].section_name, 'WorkShop')
        self.assertEqual(responseWrapper.object.sections[1].topics[0].topic_name, "openVote")
        self.assertTrue(responseWrapper.object.sections[1].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[1].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[1].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[1].topics[1].topic_name, "Future of Workshop")
        self.assertTrue(responseWrapper.object.sections[1].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[1].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[1].topics[1].possible_answers,["Cancellation", "Postpone", "Proceed"])
        self.assertTrue(responseWrapper.object.sections[1].topics[1].open_ballot)
        self.assertEqual(responseWrapper.object.sections[2].section_name, 'BEERs')
        self.assertEqual(responseWrapper.object.sections[2].topics[0].topic_name, "openVote")
        self.assertTrue(responseWrapper.object.sections[2].topics[0].votable)
        self.assertTrue(responseWrapper.object.sections[2].topics[0].yes_no_vote)
        self.assertFalse(responseWrapper.object.sections[2].topics[0].open_ballot)
        self.assertEqual(responseWrapper.object.sections[2].topics[1].topic_name, "Where")
        self.assertTrue(responseWrapper.object.sections[2].topics[1].votable)
        self.assertFalse(responseWrapper.object.sections[2].topics[1].yes_no_vote)
        self.assertEqual(responseWrapper.object.sections[2].topics[1].possible_answers,["Ombrella, Podhlato, RandomPlace"])
        self.assertTrue(responseWrapper.object.sections[2].topics[1].open_ballot)
        self.assertEqual(responseWrapper.object.sections[2].topics[2].topic_name,'Lets go')
        self.assertFalse(responseWrapper.object.sections[2].topics[2].votable)

    def test_value(self):
        """
        Tested all the argument types provided to the methods
        """
        self.assertRaises(TypeError, self.mongo.createNewAgenda, True)
        self.assertRaises(ValueError,self.mongo.createNewAgenda, {'lc':'Thessaloniki'})
        self.assertRaises(ValueError,self.mongo.createNewAgenda, {'lc':'Thessaloniki','date':'2020-03-06'})
        self.assertRaises(TypeError, self.mongo.getAgendaById, True)
        self.assertRaises(TypeError, self.mongo.updateAgenda, True, True)
        self.assertRaises(TypeError, self.mongo.updateSection, 23, 0, 'json')
        self.assertRaises(TypeError, self.mongo.updateTopic, False, 'str', True, 1)
        self.assertRaises(TypeError, self.mongo.createNewSection, 'str', 0)
        self.assertRaises(TypeError, self.mongo.createNewSectionInPosition, '15', 0, 0)
        self.assertRaises(TypeError, self.mongo.createNewTopic, True, 0,0,0)
        self.assertRaises(TypeError, self.mongo.deleteAgenda, 1251)
        self.assertRaises(TypeError, self.mongo.deleteSection, True, 'str')

    def tearDown(self) -> None:
        """
        Lets clean this up!
        """
        self.mongo.deleteAgenda(self.createdWrapper.object.id)


if __name__ == '__main__':
    unittest.main()
