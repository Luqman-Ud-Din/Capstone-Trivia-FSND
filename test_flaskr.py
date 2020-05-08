import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from constants import StatusCode
from flaskr import create_app
from models import setup_db, Category, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    question = {
        "question": "Test question",
        "answer": "Test answer",
        "category": 1,
        "difficulty": 1
    }

    updated_question = {
        "question": "Uodated Question",
        "answer": "Updated Answer",
        "category": 1,
        "difficulty": 1
    }

    def setUp(self):
        """
        Setup db.
        :param self:
        """
        self.app = create_app()
        self.client = self.app.test_client

        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.category = Category(type='Test Category')
        self.category.insert()

        self.question['category'] = int(self.category.id)
        self.updated_question['category'] = int(self.category.id)

        question = Question(**self.question)
        question.insert()

        with open('./tokens.json') as json_file:
            data = json.load(json_file)
            self.admin_headers = {
                'Authorization': 'Bearer {}'.format(data.get('admin'))
            }

            self.player_headers = {
                'Authorization': 'Bearer {}'.format(data.get('player'))
            }

        self.wrong_bearer_token = {
            'Authorization': 'Bearer {} fail'.format(data.get('member'))
        }

        self.no_token = {
            'Authorization': 'Bearer'
        }

    def tearDown(self):
        """
        Executed after reach test
        :return:
        """
        self.category.delete()

    def test_get_categories_success(self):
        """
        Success test case for get categories route.
        :return:
        """
        response = self.client().get('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_200_OK.value)
        self.assertTrue(json_data.get('success'))

    def test_get_categories_failed(self):
        """
        Fail test case for get categories route.
        :return:
        """
        response = self.client().post('/categories')
        json_data = response.get_json()
        self.assertEqual(
            response.status_code,
            StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_get_questions_success(self):
        """
        Success case for get questions.
        :return:
        """
        response = self.client().get('/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_200_OK.value)
        self.assertTrue(json_data.get('success'))

    def test_get_questions_failed(self):
        """
        Fail case for get questions.
        :return:
        """
        response = self.client().get('/questions?page=-1000')
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_404_NOT_FOUND.value
        )
        self.assertFalse(json_data.get('success'))

    def test_delete_question_success(self):
        """
        Success case of delete question test case.
        :return:
        """
        response = self.client().post('/questions', json=self.question, headers=self.admin_headers)
        json_data = response.get_json()
        response = self.client().delete(f'/questions/{json_data.get("id")}', headers=self.admin_headers)
        self.assertEqual(response.status_code, StatusCode.HTTP_204_NO_CONTENT.value)

    def test_delete_question_failed_method_not_allowed(self):
        """
        Method not allowed failed case of delete question test case.
        :return:
        """
        response = self.client().get('/questions/14')
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value)
        self.assertFalse(json_data.get('success'))

    def test_delete_question_failed_not_authorized(self):
        """
        Not authorized to delete question test case.
        :return:
        """
        response = self.client().post('/questions', json=self.question, headers=self.admin_headers)
        json_data = response.get_json()
        response = self.client().delete(f'/questions/{json_data.get("id")}', headers=self.player_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_401_UNAUTHORIZED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_delete_question_failed_not_found(self):
        """
        Not found failed case of delete question test case.
        :return:
        """
        response = self.client().delete('/questions/-1000', headers=self.admin_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_404_NOT_FOUND.value
        )
        self.assertFalse(json_data.get('success'))

    def test_add_question_success(self):
        """
        Success case of add question test case.
        :return:
        """
        response = self.client().post('/questions', json=self.question, headers=self.admin_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_201_CREATED.value
        )
        self.assertTrue(json_data.get('success'))

    def test_add_question_failed_method_not_allowed(self):
        """
        Fail case of add question test case with method not allowed error.
        :return:
        """
        response = self.client().put('/questions', json={}, headers=self.admin_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_add_question_failed_bad_request(self):
        """
        Fail case of add question test case with bad request error.
        :return:
        """
        response = self.client().post('/questions', json={}, headers=self.admin_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_400_BAD_REQUEST.value
        )
        self.assertFalse(json_data.get('success'))

    def test_add_question_failed_not_authorized(self):
        """
        Not authorized to add question.
        :return:
        """
        response = self.client().post('/questions', json=self.question, headers=self.player_headers)
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_401_UNAUTHORIZED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_get_questions_by_category_success(self):
        """
        Success case for get questions by category.
        :return:
        """
        response = self.client().get(f'/categories/{self.category.id}/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_200_OK.value)
        self.assertTrue(json_data.get('success'))

    def test_get_questions_by_category_failed_method_not_allowed(self):
        """
        Fail case for get questions by category with method not allowed error.
        :return:
        """
        response = self.client().post('/categories/1/questions')
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_get_questions_by_category_not_found(self):
        """
        Fail case for get questions by category with method not found.
        :return:
        """
        response = self.client().get('/categories/1000/questions')
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_404_NOT_FOUND.value
        )
        self.assertFalse(json_data.get('success'))

    def test_play_quiz_success(self):
        """
        Success case for play quiz api.
        :return:
        """
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        response = self.client().post('/quizzes', json=data, headers=self.player_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_200_OK.value)
        self.assertTrue(json_data.get('success'))

    def test_play_quiz_failed_method_not_allowed(self):
        """
        Fail case for play quiz api with method not allowed error.
        :return:
        """
        response = self.client().get('/quizzes', json={}, headers=self.player_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value)
        self.assertFalse(json_data.get('success'))

    def test_play_quiz_failed_bad_request(self):
        """
        Fail case for play quiz api with method bad request.
        :return:
        """
        response = self.client().post('/quizzes', json={}, headers=self.player_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, StatusCode.HTTP_400_BAD_REQUEST.value)
        self.assertFalse(json_data.get('success'))

    def test_play_quiz_failed_not_authorized(self):
        """
        Not authorized to play quiz.
        :return:
        """
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        response = self.client().post(
            '/quizzes', json=data, headers=self.wrong_bearer_token
        )
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_401_UNAUTHORIZED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_edit_question_success(self):
        """
        Success case of edit question test case.
        :return:
        """
        response = self.client().post(
            '/questions', json=self.question, headers=self.admin_headers
        )

        question_id = response.get_json().get('id')
        response = self.client().patch(
            f'/questions/{question_id}', json=self.updated_question,
            headers=self.admin_headers
        )

        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_200_OK.value
        )
        self.assertTrue(json_data.get('success'))

    def test_edit_question_failed_method_not_allowed(self):
        """
        Fail case of edit question test case with method not allowed error.
        :return:
        """
        response = self.client().put(
            '/questions', json={}, headers=self.admin_headers
        )
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_405_METHOD_NOT_ALLOWED.value
        )
        self.assertFalse(json_data.get('success'))

    def test_edit_question_failed_bad_request(self):
        """
        Fail case of edit question test case with bad request error.
        :return:
        """
        response = self.client().patch(
            '/questions/1000', json={}, headers=self.admin_headers
        )
        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_404_NOT_FOUND.value
        )
        self.assertFalse(json_data.get('success'))

    def test_edit_question_failed_not_authorized(self):
        """
        Not authorized to edit question.
        :return:
        """
        response = self.client().post(
            '/questions', json=self.question, headers=self.admin_headers
        )

        question_id = response.get_json().get('id')
        response = self.client().patch(
            f'/questions/{question_id}', json=self.updated_question,
            headers=self.player_headers
        )

        json_data = response.get_json()
        self.assertEqual(
            response.status_code, StatusCode.HTTP_401_UNAUTHORIZED.value
        )
        self.assertFalse(json_data.get('success'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
