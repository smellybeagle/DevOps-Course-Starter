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

docker run --env-file .env -p 5000:5000 todo-app:dev
docker run --env-file .env -p 8000:8000 todo-app:prod

### DockerHub
The image created can be stored in DockerHub:
$ docker build --target production --tag smellybeagle:latest .
$ docker tag smellybeagle:latest lvarnham/smellybeagle:latest 
$ docker push lvarnham/smellybeagle:latest 

https://hub.docker.com/layers/lvarnham/smellybeagle/latest/



Now visit in your web browser to view the app.
Production: [`http://localhost:8000/`](http://localhost:8000/) 
Development:[`http://localhost:5000/`](http://localhost:5000/)


### Testing The Application

The application is tested in GitHub by GitHub Action workflows whenever the application is commited.
To view the tests, go to https:\\github.com\<accountname>\<repository>\actions

