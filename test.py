from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """stuff to do on mount"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_root(self):
        """test homepage for correct HTML"""

        with self.client as client:
            response = client.get('/')
            self.assertIn('board', session)

            high_score = session.get('high_score', 0)
            count = session.get('count', 0)

            self.assertIn(f'<b id="high-score">{high_score}</b>'.encode('utf-8'), response.data)
            self.assertIn(f'<b id="count">{count}</b>'.encode('utf-8'), response.data)

    def test_word(self):
        """test if word is on the board or not"""

        with self.client as client:
            with client.session_transaction() as client_session:
                client_session['board'] = [['D', 'O', 'G', 'O', 'D'],
                                           ['D', 'O', 'G', 'O', 'D'],
                                           ['D', 'O', 'G', 'O', 'D'],
                                           ['D', 'O', 'G', 'O', 'D'],
                                           ['D', 'O', 'G', 'O', 'D']]
        response = self.client.get('/check/dog')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check/caterpillar')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_word(self):
        """test invalid word"""

        self.client.get('/')
        response = self.client.get(
            '/check/this-is-not-a-word')
        self.assertEqual(response.json['result'], 'not-word')
