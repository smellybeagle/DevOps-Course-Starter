# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements
Docker Desktop
Python Docker Image
Poetry
Flask
gunicorn
github

## Dependencies
Create a docker hub account
Install Docker Desktop
Download a suitable image, something like Alpine

## Running the App
run the following:
$ docker build --target development --tag todo-app:dev .
$ docker build --target production --tag todo-app:prod .

Now visit in your web browser to view the app.
Production: [`http://localhost:8000/`](http://localhost:8000/) 
Development:[`http://localhost:5000/`](http://localhost:5000/)


### Testing The Application

Install dependency PYTEST
```bash
$ poetry add pytest
```

There are 2 tests integrated with this application, 1 to do a basic model test and the other to test the API calls.
The testing simulates the application being created and run without making external calls.
##todo_app\tests\test_view_model.py
This test proves the application model is valid

##todo_app\tests\test_client.py
This test simulates the Trello API calls and utilises test sample data as returned data.
```bash
$ poetry run pytest
```
