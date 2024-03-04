import os
import unittest
import json
import logging

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
TEST_DB_NAME = os.getenv('DB_TEST_NAME')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, TEST_DB_NAME)

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TO/DO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # PASS
    # curl http://127.0.0.1:5000/categories
    def test_retrieve_categories(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().get('/categories')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200) ##
        self.assertTrue(data['categories'])

    # PASS
    # curl http://127.0.0.1:5000/questions
    # curl http://127.0.0.1:5000/questions?page=1
    def test_retrieve_questions(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        #self.assertTrue(data['categories']) ##

    # FIXME AssertionError: 422 != 404
    # curl http://127.0.0.1:5000/questions?page=999
    def test_404_retrieve_questions(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 404) ##
        self.assertEqual(data['success'], False)

    # FIXME AssertionError: 422 != 200
    # curl -X DELETE http://127.0.0.1:5000/questions/1
    def test_delete_question(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200) ##
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['success'])
        self.assertEqual(question, None)

    # FIXME AssertionError: 422 != 404
    # curl -X DELETE http://127.0.0.1:5000/questions/999
    def test_404_delete_question(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # PASS
    # curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Test question", "answer":"Test answer", "category":1, "difficulty":4}'
    def test_create_question(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/questions', json={
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 4
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])

    # FIXME
    # curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Test question"}'
    def test_422_create_question(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/questions', json={
            'question': 'Test question'
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # FIXME AssertionError: 422 != 200
    # curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
    def test_search_questions(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/questions/search', json={
            'search_term': 'title'
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # FIXME 
    # curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":''}'
    def test_422_search_questions(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/questions/search', json={
            'search_term': None
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # FIXME AssertionError: 422 != 200
    # curl http://127.0.0.1:5000/categories/1/questions
    def test_retrieve_questions_in_category(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Science')

    # FIXME AssertionError: 422 != 404
    # curl http://127.0.0.1:5000/categories/999/questions
    def test_404_retrieve_questions_in_category(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 404) ##
        self.assertEqual(data['success'], False)

    # FIXME AssertionError: 422 != 200
    # curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [47], "quiz_category": {"type": "Geography", "id": "3"}}'
    def test_play_quiz(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/quizzes', json={
            'previous_questions': [3, 4],
            'quiz_category': {
                'id': 6
            }
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 200) ##
        self.assertTrue(data['question'])

    # FIXME AssertionError: 422 != 404
    # 
    def test_404_play_quiz(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/quizzes', json={
            'previous_questions': [3, 4],
            'quiz_category': {
                'type': "Dance",
                'id': 999
            }
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": None, "quiz_category": None}'
    def test_422_play_quiz(self):
        logging.basicConfig(level=logging.INFO)
        res = self.client().post('/quizzes', json={
            'previous_questions': None,
            'quiz_category': {
                'id': None
            }
        })
        data = json.loads(res.data)

        logging.info("Response data: %s", data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
