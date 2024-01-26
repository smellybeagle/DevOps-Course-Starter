# Create stage for Poetry installation
FROM python as poetry-base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Dependencies
RUN pip install pytest


# install poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# copy only pyproject.toml and poetry.lock file nothing else here
COPY poetry.lock pyproject.toml ./

# this will create the folder /app/.venv (might need adjustment depending on which poetry version you are using)
RUN poetry config virtualenvs.create false --local && poetry install
#RUN poetry install --no-root --no-ansi --without dev

# Create a new stage from the base python image
FROM poetry-base as production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"


WORKDIR /app
# copy the venv folder from builder image 
#COPY --from=poetry-base /app/.venv ./.venv
# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# Install Dependencies
RUN pip install gunicorn

# Copy Application
COPY . /app
#COPY .env /app/todo_app

# Run Application
EXPOSE 8000


CMD [ "poetry", "run", "python", "-m", "gunicorn","todo_app.app:create_app()" ,"--bind","0.0.0.0"]

# Create a new stage from the base python image
FROM poetry-base as development

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"


WORKDIR /app
# copy the venv folder from builder image 
COPY --from=poetry-base /app/.venv ./.venv
# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# Install Dependencies
RUN pip install gunicorn

# Copy Application
COPY . /app

# Run Application
EXPOSE 5000

#CMD [ "poetry", "run", "python", "-m", "gunicorn","todo_app.app:create_app()" ,"--bind","0.0.0.0"]
CMD [ "poetry", "run", "flask", "run", "--host","0.0.0.0"]

# Create a new stage from the base python image
FROM poetry-base as test

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"


WORKDIR /app
# copy the venv folder from builder image 
COPY --from=poetry-base /app/.venv ./.venv
# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# Install Dependencies
RUN pip install gunicorn

# Copy Application
#COPY . /app
COPY .env.test /app/todo_app
COPY .env.template /app/todo_app

# Run Application
EXPOSE 8100

ENTRYPOINT ["poetry", "run", "pytest"]