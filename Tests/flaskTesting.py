import requests
import unittest
from BasicClasses.Agenda import *


class FlaskTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_url = "http://127.0.0.1:5000/"

        agenda_params = {"date": "03-01-2017", "lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=agenda_params)

        self.agenda_id = response.json().get("agenda").get("id")

        section_params = {"agenda_id": self.agenda_id, "section_name": "gmElections"}
        requests.post(self.basic_url + "create-section", json=section_params)

        section_params = {"agenda_id": self.agenda_id, "section_name": "Workshop"}
        requests.post(self.basic_url + "create-section", json=section_params)

        section_params = {"agenda_id": self.agenda_id, "section_name": "Krasia"}
        requests.post(self.basic_url + "create-section", json=section_params)

        new_topic = {'topic_name': 'openGmStaffEl', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 0, "topic_position": 0,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'MinutesElection', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Marios', 'Tasos', 'urMOM'], 'open_ballot': True}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 0, "topic_position": 1,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'openVote', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 1, "topic_position": 0,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Future of Workshop', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Cancelation', 'Postpone', 'proceed'], 'open_ballot': True}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 1, "topic_position": 1,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'openVote', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 2, "topic_position": 0,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Wanna go ?', 'votable': True, 'yes_no_vote': True, 'open_ballot': True}
        topic_params = {"id": self.agenda_id, "section_position": 2, "topic_position": 1, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Where', 'votable': True, 'yes_no_vote': False,
                     'possible_answers': ['Omprella, Podhlato, SomeWeirdAssPlace'], 'open_ballot': True}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 2, "topic_position": 2,
                        "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        new_topic = {'topic_name': 'Lets go', 'votable': False}
        topic_params = {"agenda_id": self.agenda_id, "section_position": 2, "topic_position": 3,
                        "topic_json": new_topic}
        final_response = requests.post(self.basic_url + "create-topic", json=topic_params)

    def test_createAgenda(self):
        params = {"date": "03-01-2017", "lc": "Thess"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 200)

        params = {"date": "03-01-2017"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"lc": "Thess"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"date": "23/01/20"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 400)  # It should return 500 or 501

    def test_createSection(self):
        params = {"agenda_id": self.agenda_id}
        response = requests.post(self.basic_url + "create-section", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"agenda_id": "123456789012345678901234", "section_name": "Beers"}
        response = requests.post(self.basic_url + "create-section", json=params)
        self.assertEqual(response.json().get("response"), 404)

        params = {"agenda_id": self.agenda_id, "section_name": "Beers"}
        response = requests.post(self.basic_url + "create-section", json=params)
        self.assertEqual(response.json().get("response"), 200)

        agenda = getAgendaFromJson(response.json().get("agenda"))
        self.assertEqual(agenda.sections[-1].section_name, "Beers")

    def test_createTopic(self):
        # In request gets only agenda_id
        params = {"agenda_id": self.agenda_id}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        # In request gets only section_position
        params = {"section_position": 0}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        # In request gets only agenda_id, section_position
        params = {"agenda_id": self.agenda_id, "section_position": 0}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        topic = {'topic_name': 'Workshop', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}

        # In request gets only section_position, topic_position, topic_json
        params = {"section_position": 0, " topic_position": 0, "topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        # In request gets only agenda_id, topic_position, topic_json
        params = {"agenda_id": self.agenda_id, " topic_position": 0, "topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        # In request gets only topic_position, topic_json
        params = {" topic_position": 0, "topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        # In request gets only topic_json
        params = {"topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"agenda_id": "123456789012345678901234", "section_position": 0, " topic_position": 0,
                  "topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"agenda_id": self.agenda_id, "section_position": 3, " topic_position": 0, "topic_json": topic}
        response = requests.post(self.basic_url + "create-topic", json=params)
        self.assertEqual(response.json().get("response"), 400)  # Expected value should be 200

    def teardown(self) -> None:
        params = {"agenda_id": self.agenda_id}
        response = requests.post(self.basic_url + "delete-agenda", json=params)


if __name__ == '__main__':
    unittest.main()
