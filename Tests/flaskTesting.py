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


if __name__ == '__main__':
    unittest.main()
