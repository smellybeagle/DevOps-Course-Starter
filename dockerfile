FROM python:3 as base
RUN mkdir /opt/todoapp
RUN chmod 775 /opt/todoapp
WORKDIR /opt/todoapp
COPY . .
RUN pip install poetry 
# RUN poetry install
# https://project-exercises.devops.corndel.com/exercises/m8_exercise Step 4.3 You may encounter issues with Python virtual environments in containers on Azure. Adjust your Dockerfile to run Poetry without a virtualenv: use RUN poetry config virtualenvs.create false --local && poetry install instead of just RUN poetry install. There’s no need to create a virtualenv in your image anyway, as the container itself is an isolated environment.
RUN poetry config virtualenvs.create false --local && poetry install

FROM base as production
ENV environment=production
ENV WEBAPP_PORT=8000
EXPOSE ${WEBAPP_PORT}
ENTRYPOINT /usr/local/bin/poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"

FROM base as development
ENV environment=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as test
RUN apt-get update && apt-get install -y firefox-esr curl --fix-missing
ENV GECKODRIVER_VER v0.33.0
RUN curl -ksSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz
ENTRYPOINT ["poetry", "run", "pytest"]