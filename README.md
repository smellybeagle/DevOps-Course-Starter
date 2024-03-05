# DevOps Apprenticeship: Project Exercise


## System Requirements
Docker Desktop
Python Docker Image
Poetry
Flask
    -Pymongo
    -FlaskDance

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

### Security Considerations
OAUTH has been enabled to GitHub for both Localhost and the Production site.
HTTPS is enforced from the deployed Application in Azure, MongoDB is configured to accept SSL connections.
The MONGODB collection is encrypted at rest by default. Ensure the security keys are not exposed to the wider public.