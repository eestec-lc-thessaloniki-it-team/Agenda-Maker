import requests
import unittest
from BasicClasses.Agenda import *


class FlaskTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_url = "http://127.0.0.1:5000/"
        params = {"date": "27-06-2020", "lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.id = response.json().get("agenda").get("id")

    def test_createAgenda(self):
        self.basic_url = "http://127.0.0.1:5000/"
        params = {"date": "27-06-2020", "lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 200)

        params = {"date": "27-06-2020"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 400)

        params = {"lc": "Thessaloniki"}
        response = requests.post(self.basic_url + "create-agenda", json=params)
        self.assertEqual(response.json().get("response"), 400)

    def tearDown(self) -> None:
      pass

if __name__ == '__main__':
    unittest.main()
