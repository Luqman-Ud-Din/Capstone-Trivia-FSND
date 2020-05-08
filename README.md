# Full Stack Trivia API Backend


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

The application has the following features:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Update questions.
5) Play the quiz game, randomizing either all questions or within a specific category.

API Endpoints Documentation
--------------------------------------------------------
GET `'/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```json5
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

GET `'/questions'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches a list of questions.
- Request Arguments: Page Number
- Returns: Dictionary of Categories, current category, list of questions and total number of questions.

```json5
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": null,
	"questions": [
		{
			"answer": "Apollo 13",
			"category": 5,
			"difficulty": 4,
			"id": 2,
			"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		},
		{
			"answer": "Tom Cruise",
			"category": 5,
			"difficulty": 4,
			"id": 4,
			"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
		}
	],
	"total_questions": 26,
	"success": true
}
```

DELETE `'/questions/<int:question_id>'`

- Deletes question from the database.
- Request Arguments: questions_id
- Returns: true with status 204 if successfully deleted.

```json5
{
    "success": true
}
```

POST `'/questions'`

- Create a new question
- Request Body: question, answer, difficulty and category.
- Returns: true and question id with status 201 if successfully created.

Request

```json5
{
    "question": "Test question",
    "answer": "Answer",
    "category": 1,
    "difficulty": 1
}
```

Response

```json5
{
    "success": true,
    "id": 15
}
```

PATCH `'/questions<int:question_id>'`

- Updates the question.
- Request Arguments: questions_id
- Request Body: question, answer, difficulty and category.
- Returns: true and question id with status 200 if successfully updated.

Request

id=1
```json5

{
    "question": "Test question",
    "answer": "Answer",
    "category": 1,
    "difficulty": 1
}
```

Response

```json5
{
    "question": "Test question",
    "answer": "Answer",
    "category": 1,
    "difficulty": 1,
    "id": 1
}
```

POST `'/categories/<int:category_id>/questions'`

- To get questions based on category
- Request Arguments: category_id
- Returns: List of questions, total number of questions and current category.

```json5
{
	"current_category": {
		"id": 1,
		"type": "Science"
	},
	"questions": [
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		}
	],
	"total_questions": 13,
	"success": true
}
```

POST `'/quizzes'`

- In order to play the quiz.
- Returns: Random question within the given category.

Request

```json5
{
    "quiz_category": {
        "id": 1
    },
    "previous_questions": []
}
```

Response

```json5
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```

Errors
--------------------------------------------------------

Bad Request `400`

```json5
{
  'success': false,
  'error': 400,
  'message': 'Bad Request'
}
```

Unauthorized `401`

```json5
{
  'success': false,
  'error': 401,
  'message': 'Unauthorized'
}
```

Forbidden `403`

```json5
{
  'success': false,
  'error': 403,
  'message': 'Forbidden'
}
```

Not Found `404`

```json5
{
  'success': false,
  'error': 404,
  'message': 'Not Found'
}
```

Method Not Allowed `405`

```json5
{
  'success': false,
  'error': 405,
  'message': 'Method Not Allowed'
}
```

Unprocessable Entity `422`

```json5
{
  'success': false,
  'error': 422,
  'message': 'Unprocessable Entity'
}
```

Internal Server Error `500`

```json5
{
  'success': false,
  'error': 500,
  'message': 'Internal Server Error'
}
```

Permissions Documentation
--------------------------------------------------------

- `add:question` permission to add question through through POST `'/questions'` api
- `edit:question` permission to update question through PATCH `'/questions<int:question_id>'` api
- `delete:question` permission to delete question through through DELETE `'/questions<int:question_id>'` api
- `play:quiz` permission to play quiz through POST `'/quizzes'` api

Roles Documentation
--------------------------------------------------------
### Admin

Can add/update/delete question

Permissions:

- `add:question`
- `edit:question`
- `delete:question`

### Player

Can play quiz

Permissions:

- `play:quiz`

## Development environment setup

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

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

```
FLASK_APP=flaskr FLASK_ENV=development DATABASE_USER={username} DATABASE_PASSWORD={password} DATABASE_HOST=localshost DATABASE_PORT=5432 DATABASE_NAME=trivia flask run
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

Tokens to test the api end points are added in the `tokens.json` file.

The below link is used to retrieve tokens.

```
https://dev-fsnd-luqman.auth0.com/authorize?audience=trivia&response_type=token&client_id=5d2Ugz6XYfOO3Pbti83945GDmMXx4zuL&redirect_uri=http://127.0.0.1:8080/login-results
```

`admin@mail.com` has the `Admin` role and `player@mail.com` has the `Player` role.

Web app is deployed at:

```
https://trivia-capstone-demo.herokuapp.com/
```
