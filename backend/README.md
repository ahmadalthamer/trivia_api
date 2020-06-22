
# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API documentation
 - Backend is hosted locally at `http://127.0.0.1:5000/`
 - Errors results are in form of JSON file.
 - API's are handling four errors
	 * 400
	 * 404
	 * 422
	 * 500

#### GET /categories

-   resutls: Returns a list categories.
    
-   example:  `curl http://127.0.0.1:5000/categories`<br>
```
   {
	    "categories": {
	        "1": "Science", 
	        "2": "Art", 
	        "3": "Geography", 
	        "4": "History", 
	        "5": "Entertainment", 
	        "6": "Sports"
	    }, 
	    "success": true
	}
```


### GET /questions

- results: * A list of question
	       * length of the list
	       * catogries
	       * success message


- example: `curl http://127.0.0.1:5000/questoins` <br>
	```
	   "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  	},
	  "questions": [
	    {
	      "answer": "Maya Angelou",
	      "category": 4,
	      "difficulty": 2,
	      "id": 5,
	      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	    },
	   .
	   .
	   .
	   .
	   .
	  ],
	  "success": true,
	  "total_questions": 18
	}
	```

### DELETE /questions/<int:id>

- results: * success message
- exmaple: `curl http://127.0.0.1:5000/questions/6 -X DELETE`<br>

	```
	 "deleted": 6
	}
	```

### POST /questions

- results: * list of categories
		   * success message

-example : curl http://127.0.0.1:5000/questions -X POST H "Content-Type: application/json" -d '{ "question": "who is the best developer?", "answer":"Me","difficulty": "4", "category":"3"}' <br>

		```
		"categories": {
			"1": "Science",
			"2": "Art",
			"3": "Geography",
			"4": "History",
			"5": "Entertainment",
			"6": "Sports"
			},
		"success": true
		}
		```

### POST /search

- results: * list of questions
		   * total numbers of questions
		   * success message

- example: `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who is"}'`<br>

	```
		"questions": [
	    {
	      "answer": "Me",
	      "category": 4,
	      "difficulty": 3,
	      "id": 49,
	      "question": "who is the best developer?"
	    },
	    {
	      "answer": "Me",
	      "category": 4,
	      "difficulty": 3,
	      "id": 50,
	      "question": "who is the best developer?"
	    },
	    {
	      "answer": "Me",
	      "category": 4,
	      "difficulty": 3,
	      "id": 51,
	      "question": "who is the best developer?"
	    }
	  ],
	  "success": true,
	  "total_questions": 3
	}
	```


### GET /categories/<int:id>/questions

- results: * number of category
		   * list of questions
		   * total numbers
		   * success message

- example: `curl http://127.0.0.1:5000/categories/2/questions`<br>
	```
	{	"current_category": 2,
	  "questions": [
	    {
	      "answer": "Escher",
	      "category": 2,
	      "difficulty": 1,
	      "id": 16,
	      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
	    },
	    .
	    .
	    .
	    .
		   "success": true,
	  "total_questions": 3
	}
 	```


### POST /quizzes

- results:  * question
			* success message

- example `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20], "quiz_category": {"type": "Science", "id": "1"}}'`

```
{
	  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
