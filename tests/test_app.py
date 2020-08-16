import json
import unittest
from app import app
from extensions import db
from models import Result


class BasicTests(unittest.TestCase):

    # test client
    app = app.test_client()
    app.testing = True
    headers = {'Content-type': 'application/json'}

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestPostResults(BasicTests):

    def test_post_results_201(self):
        with open("tests/input.json", "r") as f:
            input_data = json.loads(f.read())
        with open("tests/output.json", "r") as f:
            output_data = json.loads(f.read())
        response = self.app.post(
            '/results',
            headers=self.headers,
            json=input_data,
        )
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 201)
