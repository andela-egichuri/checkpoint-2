<<<<<<< HEAD
[![Build Status](https://travis-ci.org/andela-egichuri/checkpoint2.svg)](https://travis-ci.org/andela-egichuri/checkpoint2) [![Coverage Status](https://coveralls.io/repos/andela-egichuri/checkpoint2/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela-egichuri/checkpoint2?branch=develop) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/b93352b105f04a4d958d1b6975b51cb4/snapshot/origin:develop:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/b93352b105f04a4d958d1b6975b51cb4)

# Checkpoint 2
Application - A Flask API for a bucket list service

## Usage Instructions:
Before installation ensure the following are installed in your system:
 - Python
 - A relational database (Postgres has been used for development and testing).

*All other dependencies are in `requirements.txt`*

* Download or clone the repo
* Install requirements.
`pip install -r requirements.txt`
* Setup environment variables
```
APP_SETTINGS="config.DevelopmentConfig"
DATABASE_URL="postgres://<user>:<password>@localhost:5432/<db_name>"
SECRET=<SECRET>
TEST_DATABASE_URL="postgres://<user>:<password>@localhost:5432/<test_db_name>"
```
* Perform database migrations.
```
python manage.py db init
python manage.py db migrate
```
* Run the application
`python app.py`

## EndPoints
Access to all endpoints except login and registration require authentication.
The login endpoint returns a token which should be added to the headers on
all other requests. The header should be given the name `token`

* **`/auth/register`**
    * POST - Creates/registers a user

* **`/auth/login`**
    * POST - Logs a user in

* **`/auth/logout`**
    * GET - Logs a user out

* **`/bucketlists/`**
    * POST - Create a new bucket list
    * GET - List all the created bucket lists

* **`/bucketlists/<id>`**
    * DELETE - Delete a given bucket list (Identified by <id>)
    * GET - Get single bucket list  (Identified by <id>)
    * PUT - Update a given bucket list  (Identified by <id>)


* **`/bucketlists/<id>/items/`**
    * POST - Create a new item in bucket list

* **`/bucketlists/<id>/items/<item_id>`**
    * PUT - Update a bucket list item
    * DELETE - Delete an item from a bucket list

## Other Functionalities
* Pagination - You can specify the number of results you wish to have returned
for bucketlists as follows.
`GET http://localhost:5000/bucketlists?limit=10`
The default number of results is 20 and the maximum number of results is 100.


* Search - To search for a bucketlist you can submit a search term as follows
`GET http://localhost:5000/bucketlists?q=hike`
All buckelists with `hike` in their name will be displayed.

## Testing
Tests are run from the root folder
`nosetests`
To include Coverage in the tests
`nosetests --with-coverage --cover-package=.`
=======
# checkpoint-2
>>>>>>> 0c77918... Initial commit
