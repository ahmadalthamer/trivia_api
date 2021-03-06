import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
	@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
	'''
    CORS(app)

    '''
	@TODO: Use the after_request decorator to set Access-Control-Allow
	'''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
	@TODO:
	Create an endpoint to handle GET requests
	for all available categories.
	'''
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = {}

        for current_category in Category.query.all():
            categories[current_category.id] = current_category.type

        if not(categories):
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })
    '''
	@TODO:
	Create an endpoint to handle GET requests for questions,
	including pagination (every 10 questions).
	This endpoint should return a list of questions,
	number of total questions, current category, categories.

	TEST: At this point, when you start the application
	you should see questions and categories generated,
	ten questions per page and pagination at the bottom of the screen for three pages.
	Clicking on the page numbers should update the questions.
	'''
    @app.route('/questions', methods=['GET'])
    def get_questions_per_page():

        questions = Question.query.all()
        pagneated_questions = paginate_questions(request, questions)

        categories = {}
        for current_category in Category.query.all():
            categories[current_category.id] = current_category.type

        if (len(pagneated_questions) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': pagneated_questions,
            'total_questions': len(questions),
            'categories': categories
        })
    '''
	@TODO:
	Create an endpoint to DELETE question using a question ID.

	TEST: When you click the trash icon next to a question, the question will be removed.
	This removal will persist in the database and when you refresh the page.
	'''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).first()

        if question is None:
            return abort(404)

        question.delete()

        return jsonify({
            'deleted': question_id,
            'success': True
        })

    '''
	@TODO:
	Create an endpoint to POST a new question,
	which will require the question and answer text,
	category, and difficulty score.

	TEST: When you submit a question on the "Add" tab,
	the form will clear and the question will appear at the end of the last page
	of the questions list in the "List" tab.
	'''
    @app.route('/questions', methods=['POST'])
    def post_question():

        body = request.get_json()

        if not ('question' in body and 'answer' in body):
            abort(422)

        new_question = Question(
            question=body['question'],
            answer=body['answer'],
            difficulty=body['difficulty'],
            category=body['category'])
        new_question.insert()
        tmp = {}
        tmp['id'] = new_question.id
        tmp['question'] = new_question.question
        tmp['answer'] = new_question.answer
        tmp['difficulty'] = new_question.difficulty
        tmp['category'] = new_question.category

        return jsonify({
            'success': True,
            'question': tmp
        })

    '''
	@TODO:
	Create a POST endpoint to get questions based on a search term.
	It should return any questions for whom the search term
	is a substring of the question.

	TEST: Search by any phrase. The questions list will update to include
	only question that include that string within their question.
	Try using the word "title" to start.
	'''
    @app.route('/search', methods=['POST'])
    def search():

        body = request.get_json()
        tmp = body['searchTerm']

        if (tmp == ""):
            abort(422)

        search_results = Question.query.filter(
            Question.question.ilike(f'%{tmp}%')).all()

        data = []
        for details in search_results:
            tmp = {}
            tmp['id'] = details.id
            tmp['question'] = details.question
            tmp['answer'] = details.answer
            tmp['difficulty'] = details.difficulty
            tmp['category'] = details.category
            data.append(tmp)

        return jsonify({
            'success': True,
            'questions': data,
            'total_questions': len(data)
        })
    '''
	@TODO:
	Create a GET endpoint to get questions based on category.

	TEST: In the "List" tab / main screen, clicking on one of the
	categories in the left column will cause only questions of that
	category to be shown.
	'''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):

        category = Question.query.filter_by(category=category_id).all()

        if (len(category) == 0):
            abort(404)

        data = []
        for details in category:
            tmp = {}
            tmp['id'] = details.id
            tmp['question'] = details.question
            tmp['answer'] = details.answer
            tmp['difficulty'] = details.difficulty
            tmp['category'] = details.category
            data.append(tmp)

        return jsonify({
            'success': True,
            'questions': data,
            'total_questions': len(data),
            'current_category': category_id
        })

    '''
	@TODO:
	Create a POST endpoint to get questions to play the quiz.
	This endpoint should take category and previous question parameters
	and return a random questions within the given category,
	if provided, and that is not one of the previous questions.

	TEST: In the "Play" tab, after a user selects "All" or a category,
	one question at a time is displayed, the user is allowed to answer
	and shown whether they were correct or not.
	'''
    @app.route('/quizzes', methods=['POST'])
    def get_quizz():
        payload = request.get_json()

        if not(('previous_questions' in payload)
                or ('quiz_category' is payload)):
            abort(422)

        if (payload['quiz_category']['id'] == 0):
            questions = Question.query.filter(
                Question.id.notin_(
                    (payload['previous_questions']))).order_by(
                func.random()).first()
        else:
            questions = Question.query.filter_by(
                category=payload['quiz_category']['id']).filter(
                Question.id.notin_(
                    (payload['previous_questions']))).order_by(
                func.random()).first()

        print(questions, file=sys.stderr)
        tmp = {}
        tmp['id'] = questions.id
        tmp['question'] = questions.question
        tmp['answer'] = questions.answer
        tmp['difficulty'] = questions.difficulty
        tmp['category'] = questions.category

        return jsonify({
            'success': True,
            'question': tmp
        })
    '''
	@TODO:
	Create error handlers for all expected errors
	including 404 and 422.
	'''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'system is down try again'
        }), 500

    return app
