# Create stage for Poetry installation
FROM python as poetry-base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# copy only pyproject.toml and poetry.lock file nothing else here
COPY poetry.lock pyproject.toml ./

# this will create the folder /app/.venv (might need adjustment depending on which poetry version you are using)
RUN poetry install --no-root --no-ansi --without dev

# Create a new stage from the base python image
FROM poetry-base as todo-app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"


WORKDIR /app
# copy the venv folder from builder image 
COPY --from=poetry-base /app/.venv ./.venv
# Copy Dependencies
COPY poetry.lock pyproject.toml .venv ./

# [OPTIONAL] Validate the project is properly configured
#RUN poetry check

# Install Dependencies
RUN pip install gunicorn
#RUN poetry install --no-interaction --no-cache --without dev

# Copy Application
COPY . /app
COPY .env /app/todo_app
# Run Application
##poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"
EXPOSE 5000
RUN poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"
#CMD [ "poetry", "run", "python", "-m", "gunicorn", "run", "--host=0.0.0.0" ]
#CMD [ "poetry", "run", "gunicorn", "--bind 0.0.0.0" ]