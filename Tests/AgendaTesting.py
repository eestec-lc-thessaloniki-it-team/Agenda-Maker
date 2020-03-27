import unittest
from BasicClasses.Topic import Topic
from BasicClasses.Agenda import *
from BasicClasses.Section import Section


class AgendaTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.json = {'date': '23-3-20', 'id': '001', 'lc': 'Thessaloniki',
                     'sections': [{'section_name': 'gmElections', 'topics': [
                         {'topic_name': 'openGmstaffEl', 'votable': True,
                          'yes_no_vote': True, 'open_ballot': False},
                         {'topic_name': 'MinutesElection', 'votable': True,
                          'yes_no_vote': False,
                          'possible_answers': ['Marios', 'Tasos', 'urMOM'],
                          'open_ballot': True}]}, {'section_name': 'WorkShop',
                                                   'topics': [
                                                       {'topic_name': 'openVote',
                                                        'votable': True,
                                                        'yes_no_vote': True,
                                                        'open_ballot': False}, {
                                                           'topic_name': 'Future of Workshop',
                                                           'votable': True,
                                                           'yes_no_vote': False,
                                                           'possible_answers': [
                                                               'Cancelation',
                                                               'Postpone', 'proceed'],
                                                           'open_ballot': True}]},
                                  {'section_name': 'Krasia', 'topics': [
                                      {'topic_name': 'openVote', 'votable': True,
                                       'yes_no_vote': True, 'open_ballot': False},
                                      {'topic_name': 'Wanna go ?', 'votable': True,
                                       'yes_no_vote': True, 'open_ballot': True},
                                      {'topic_name': 'Where', 'votable': True,
                                       'yes_no_vote': False, 'possible_answers': [
                                          'Omprella, Podhlato, SomeWeirdAssPlace'],
                                       'open_ballot': True},
                                      {'topic_name': 'Lets go', 'votable': False}]}]}
        self.gmElectionsTopics = [Topic("openGmstaffEl", True, True, False, ),
                                  Topic("MinutesElection", True, False, True, ["Marios", "Tasos", "urMOM"])]
        self.WorkshopTopics = [Topic("openVote", True, True, False),
                               Topic("Future of Workshop", True, False, True, ["Cancelation", "Postpone", "proceed"])]
        self.KrasiaTopics = [Topic("openVote", True, True, False), Topic("Wanna go ?", True, True, True),
                             Topic("Where", True, False, True, ["Omprella, Podhlato, SomeWeirdAssPlace"]),
                             Topic("Lets go", False)]
        self.MemberTopic = Topic("Promoted by attending GMs", False)
        self.newMemberTopic = Topic("Promoted by organizing an event", False)
        self.TichuTopic = [Topic("Tichu", False)]
        self.CAHTopic = Topic("Cards Against Humanity", False)

        self.section1 = Section("gmElections", self.gmElectionsTopics)
        self.section2 = Section("WorkShop", self.WorkshopTopics)
        self.section3 = Section("Krasia", self.KrasiaTopics)
        self.section4 = Section("Quarantine Games", self.TichuTopic)
        self.sections = [self.section1, self.section2, self.section3]

        self.agenda = Agenda("23-3-20", "001", "Thessaloniki", self.sections)

    def test_makeJson(self):
        self.assertDictEqual(self.agenda.makeJson(), self.json)

    def test_getAgendaFromJson(self):
        self.assertEqual(getAgendaFromJson(self.json), self.agenda)

    def test_addSection(self):
        section_name = "Member Promotions"
        self.assertTrue(self.agenda.addSection(section_name))
        self.assertTrue(len(self.agenda.sections) == 4)
        self.assertEqual(self.agenda.sections[3].section_name, section_name)

        self.assertFalse(self.agenda.addSection(section_name))  #
        self.assertTrue(len(self.agenda.sections) == 4, "Should not add it again")

    def test_addTopic(self):
        len_section1 = len(self.agenda.sections[0].topics)
        self.assertTrue(self.agenda.addTopic(0, self.MemberTopic))
        self.assertEqual(len(self.agenda.sections[0].topics), len_section1 + 1)
        self.assertTrue(self.MemberTopic in self.agenda.sections[0].topics)
        self.assertEqual(self.agenda.sections[0].topics[-1], self.MemberTopic)

    def test_addTopicInPosition(self):
        len_section1 = len(self.agenda.sections[0].topics)
        self.assertTrue(self.agenda.addTopicInPosition(0, self.newMemberTopic, 0))
        self.assertEqual(self.agenda.sections[0].topics[0], self.newMemberTopic)
        self.assertEqual(len(self.agenda.sections[0].topics), len_section1 + 1)

    def test_addTopicToWrongPosition(self):
        len_section1 = len(self.agenda.sections[0].topics)
        self.assertFalse(self.agenda.addTopicInPosition(0, self.newMemberTopic, len_section1 + 3))
        self.assertEqual(len(self.agenda.sections[0].topics), len_section1)

    def test_deleteTopic(self):
        len_section1 = len(self.agenda.sections[0].topics)
        topic_in_0_0 = self.agenda.sections[0].topics[0]
        self.assertTrue(self.agenda.deleteTopic(0, 0))
        self.assertNotEqual(topic_in_0_0, self.agenda.sections[0].topics[0])
        self.assertEqual(len(self.agenda.sections[0].topics), len_section1 - 1)

    def test_deleteSection(self):
        sections = len(self.agenda.sections)
        self.assertTrue(self.agenda.deleteSection(-1))
        self.assertTrue(len(self.agenda.sections), sections - 1)

    def test_addSectionInPosition(self):
        sections = len(self.agenda.sections)
        previousInPosition = self.agenda.sections[1]
        section_name = "My Section"
        self.assertTrue(self.agenda.addSectionInPosition(section_name, 1))
        self.assertEqual(self.agenda.sections[1].section_name, section_name)
        self.assertEqual(len(self.agenda.sections), sections + 1)
        self.assertEqual(self.agenda.sections[2], previousInPosition)

    def test_addSectionInWrongPosition(self):
        sections = len(self.agenda.sections)
        section_name = "My Section"
        self.assertFalse(self.agenda.addSectionInPosition(section_name, sections + 3))
        self.assertEqual(len(self.agenda.sections), sections)

    def test_setSection(self):
        sections = len(self.agenda.sections)
        self.assertTrue(self.agenda.setSection(2, self.section4))
        self.assertEqual(len(self.agenda.sections), sections)
        self.assertEqual(self.agenda.sections[2], self.section4)
        # test it in wrong position
        self.assertFalse(self.agenda.setSection(10, self.section4))
        self.assertEqual(len(self.agenda.sections), sections)

    def test_setTopic(self):
        topics = self.agenda.sections[1].topics
        self.assertTrue(self.agenda.setTopic(1, 0, self.CAHTopic))
        self.assertEqual(len(self.agenda.sections[1].topics), len(topics))
        self.assertEqual(self.agenda.sections[1].topics[0], self.CAHTopic)
        # add it with negative position
        self.assertTrue(self.agenda.setTopic(1,-1,self.TichuTopic))
        self.assertEqual(self.agenda.sections[1].topics[-1],self.TichuTopic)
        # add it in wrong position
        self.assertFalse(self.agenda.setTopic(1,10,self.CAHTopic))
        self.assertEqual(len(self.agenda.sections[1].topics), len(topics))


if __name__ == '__main__':
    unittest.main()
