import requests
import unittest
from BasicClasses.Agenda import *


class FlaskTesting(unittest.TestCase):

    def test_createAgenda(self):
        self.basic_url = "http://127.0.0.1:5000/"
        params = {"date": "27-06-2020", "lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        data = response.json()
        print(data)

    def test_updateSection(self):
        self.basic_url = "http://127.0.0.1:5000/"

        agenda_params = {"date": "27-04-2020", "lc": "Thessaloniki"}
        agenda_response = requests.post(self.basic_url + "create-agenda", json=agenda_params)

        agenda_id = agenda_response.json().get("agenda").get("id")

        create_params = {"id": agenda_id, "section_name": "quarantine_ends"}
        requests.post(self.basic_url + "create-section", json=create_params)

        new_section = {"section_name": "quarantine_over", "topics": []}
        params = {"agenda_id": agenda_id, "section_position": 0, "section_json": new_section}
        response = requests.post(self.basic_url + "update-section", json=params)
        data = response.json()
        print(data)

    def test_deleteTopic(self):
        self.basic_url = "http://127.0.0.1:5000/"
        
        agenda_params = {"date": "27-04-2020", "lc": "Thessaloniki"}
        agenda_response = requests.post(self.basic_url + "create-agenda", json=agenda_params)

        agenda_id = agenda_response.json().get("agenda").get("id")

        section_params = {"id": agenda_id, "section_name": "quarantine_ends"}
        requests.post(self.basic_url + "create-section", json=section_params)

        new_topic = {'topic_name': 'openGmStaffEl', 'votable': True, 'yes_no_vote': True, 'open_ballot': False}
        topic_params = {"id": agenda_id, "section_position": 0, "topic_position": 0, "topic_json": new_topic}
        requests.post(self.basic_url + "create-topic", json=topic_params)

        params = {"agenda_id": agenda_id, "section_position": 0, "topic_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        data = response.json()
        print(data)


if __name__ == '__main__':
    unittest.main()
