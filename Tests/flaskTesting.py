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
        print(agenda_response.json())
        create_params = {"id": str(agenda_response.json().get("agenda").get("id")),
                         "section_name": "quarantine_ends"}
        create_response = requests.post(self.basic_url + "create-section", json=create_params)
        print(create_response.json().get("response"))
        params = {"agenda_id": create_response.json().get("agenda").get("id"), "section_position": 0,
                  "section_json": {"section_name": "quarantine_over", "topics": []}}
        response = requests.post(self.basic_url + "update-section", json=params)
        data = response.json()
        print(data)

    def test_deleteTopic(self):
        self.basic_url = "http://127.0.0.1:5000/"
        params = {"agenda_id": 1, "section_position": 0, "topic_position": 0}
        response = requests.post(self.basic_url + "delete-topic", json=params)
        data = response.json()
        print(data)


if __name__ == '__main__':
    unittest.main()
