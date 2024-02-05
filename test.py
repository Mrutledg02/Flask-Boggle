from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index_route(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<table id="boggle-board">', response.data)

    def test_set_board_size_route(self):
        with self.client:
            response = self.client.get('/set_board_size')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Enter the size of the Boggle board:', response.data)

    def test_check_word_route_valid_word(self):
        with self.client:
            with app.test_request_context():
                # Set up a mock board in the session
                boggle_game = Boggle(size=3)
                session['board'] = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
                
                # Mock a valid word in the session
                session['words'] = ['ABC']
                
                response = self.client.post('/check_word', json={'word': 'ABC'})
                data = response.get_json()
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(data['result'], 'ok')
                self.assertIn(b'Valid word on the board!', response.data)

    def test_check_word_route_invalid_word(self):
        with self.client:
            with app.test_request_context():
                # Set up a mock board in the session
                boggle_game = Boggle(size=3)
                session['board'] = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
                
                # Mock an invalid word in the session
                session['words'] = ['XYZ']
                
                response = self.client.post('/check_word', json={'word': 'XYZ'})
                data = response.get_json()
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(data['result'], 'not-on-board')
                self.assertIn(b'Word is not on the board.', response.data)

    def test_end_game_route(self):
        with self.client:
            with app.test_request_context():
                # Set up a mock score in the session
                session['score'] = 10
                
                response = self.client.post('/end_game', json={'score': 10})
                data = response.get_json()
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(data['message'], 'Game ended successfully')
                self.assertEqual(session['num_played'], 1)
                self.assertEqual(session['highest_score'], 10)
