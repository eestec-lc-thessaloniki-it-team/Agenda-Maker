import requests
import unittest
from BasicClasses.Agenda import *


class FlaskTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_url = "http://127.0.0.1:5000/"

        agenda_params = {"date": "23-03-20", "lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=agenda_params)

        self.agenda_id = response.json().get("agenda").get("id")

        section_params = {"id": self.agenda_id, "section_name": "gmElections"}
        requests.post(self.basic_url + "create-section", json=section_params)

        section_params = {"id": self.agenda_id, "section_name": "Workshop"}
        requests.post(self.basic_url + "create-section", json=section_params)

        section_params = {"id": self.agenda_id, "section_name": "Krasia"}
        requests.post(self.basic_url + "create-section", json=section_params)

        new_topic = {'topic_name': 'openGmStaffEl', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"id": self.agenda_id, "section_position": 0, "topic_position": 0, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'MinutesElection', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Marios', 'Tasos', 'urMOM'], 'open_ballot': True}
        topic_params = {"id": self.agenda_id, "section_position": 0, "topic_position": 1, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'openVote', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"id": self.agenda_id, "section_position": 1, "topic_position": 0, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Future of Workshop', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Cancelation', 'Postpone', 'proceed'], 'open_ballot': True}
        topic_params = {"id": self.agenda_id, "section_position": 1, "topic_position": 1, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'openVote', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"id": self.agenda_id, "section_position": 2, "topic_position": 0, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Wanna go ?', 'votable': True, 'yes_no_vote': True, 'open_ballot': True}
        topic_params = {"id": self.agenda_id, "section_position": 2, "topic_position": 1, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Where', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Omprella, Podhlato, SomeWeirdAssPlace'], 'open_ballot': True}
        topic_params = {"id": self.agenda_id, "section_position": 2, "topic_position": 2, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Lets go', 'votable': False}
        topic_params = {"id": self.agenda_id, "section_position": 2, "topic_position": 3, "topic_json": new_topic}
        final_response = requests.post(self.basic_url + "create-topic", json=topic_params)

        data = final_response.json()
        print(data)

    def test_updateSection(self):
        new_section = {"section_name": "QuarantineGames", "topics": []}

        params = {"agenda_id": self.agenda_id, "section_position": 0}
        response = requests.post(self.basic_url + "update-section", json=params)
        self.assertTrue(response.json().get("response"), 400)

        params = {"agenda_id": "5e8d8b26ad0789ce0a9d84b6", "section_position": 0, "section_json": new_section}
        response = requests.post(self.basic_url + "update-section", json=params)
        self.assertTrue(response.json().get("response"), 404)

        params = {"agenda_id": self.agenda_id, "section_position": 7, "section_json": new_section}
        response = requests.post(self.basic_url + "update-section", json=params)
        self.assertTrue(response.json().get("response"), 501)

        params = {"agenda_id": self.agenda_id, "section_position": 0, "section_json": new_section}
        response = requests.post(self.basic_url + "update-section", json=params)
        self.assertTrue(response.json().get("response"), 200)
        agenda = getAgendaFromJson(response.json().get("agenda"))
        self.assertEqual(agenda.sections[0], getSectionFromJson(new_section))

        data = response.json()
        print(data)

    def test_deleteTopic(self):
        params = {"agenda_id": self.agenda_id, "section_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"agenda_id": "123456789012345678901234", "section_position": 0, "topic_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        self.assertEqual(response.json().get("response"), 404)

        params = {"agenda_id": self.agenda_id, "section_position": 7, "topic_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        self.assertEqual(response.json().get("response"), 501)  # TODO: change to return 4** when operation is not done

        new_topic = {'topic_name': 'Tichu', 'votable': False}
        topic_params = {"id": self.agenda_id, "section_position": 0, "topic_position": 0, "topic_json": new_topic}
        response = requests.post(self.basic_url + "create-topic", json=topic_params)
        old_agenda = getAgendaFromJson(response.json().get("agenda"))

        params = {"agenda_id": self.agenda_id, "section_position": 0, "topic_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        data = response.json()
        self.assertEqual(data.get("response"), 200)

        new_agenda = getAgendaFromJson(data.get("agenda"))
        self.assertNotEqual(old_agenda.sections[0].topics[0], new_agenda.sections[0].topics[0])

    def tearDown(self) -> None:
        params = {"id": self.agenda_id}
        response = requests.post(self.basic_url + "delete-agenda", json=params)
        print(response.json().get("response"))


if __name__ == '__main__':
    unittest.main()
