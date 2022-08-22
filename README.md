#Social Network
##Introduction
The goal of this project is to provide a social platform where user can sign up account and creat posts. User can also edit and delete their post. User can like and unlike other users posts.
###Setup

The first thing to do is to clone the repository:
```
$ git clone https://github.com/adnan9867/backend.git
$ cd backend
```
Create a virtual environment to install dependencies in and activate it:
run following command to install python-env

```
$ sudo apt-get install python3-venv  
$ mkdir djangoenv
```

creat and activate virtual environment
```
$ python3 -m venv djangoenv 
$ source djangoenv/bin/activate 
```
Then install the dependencies:

```
(env)$ pip install -r requirements.txt
```

After installing dependencies run following command to migrate changes in db:

```
(env)$ python manage.py migrate
```

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment:

Now run following command to runserver:
```
(env)$ python manage.py runserver
```

##Execute Tests

All Api's endpoints are covered with test cases: 
After project setup run following command to execute tests.

```
(env)$ pytest
```

By executing this command you can run all test cases.

