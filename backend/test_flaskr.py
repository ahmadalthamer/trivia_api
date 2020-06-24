import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'Ahmad@123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories(self):
        result = self.client().get('/categories/1000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_per_page(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_get_questions_per_page_beyond_index(self):
        result = self.client().get('/questions?page=1000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # make sure to modify the number of the question to existing one
    def test_delete_question(self):
        question = Question(question='test', answer='test',
                            difficulty=1, category=1)
        question.insert()

        result = self.client().delete('/questions/{}'.format(question.id))
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question.id)

    def test_404_delete_question(self):
        result = self.client().delete('/questions/1000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_book(self):
        test = {
            'question': 'test',
            'answer': 'test',
            'difficulty': 1,
            'category': 1
        }
        result = self.client().post('/questions', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))

    def test_422_create_new_book(self):
        test = {
            'question': 'test',
            'difficulty': 1,
            'category': 1
        }
        result = self.client().post('/questions', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search(self):
        test = {
            'searchTerm': 'what'
        }

        result = self.client().post('/search', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_422_search(self):
        test = {
            'searchTerm': "",
        }

        result = self.client().post('/search', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_get_by_category(self):

        result = self.client().get('/categories/2/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_by_category(self):

        result = self.client().get('/categories/10000/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_quizz(self):

        test = {
            "previous_questions": [],
            "quiz_category": {
                "type": "Science",
                "id": "1"}}

        result = self.client().post('/quizzes', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_get_quizz(self):

        test = {"quiz_category": {"type": "Science", "id": "1"}}

        result = self.client().post('/quizzes', json=test)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
