import json
from dotenv import load_dotenv, find_dotenv
from flask.testing import FlaskClient
import mongomock
import requests
import pytest
from pytest import MonkeyPatch
from todo_app import app
from flask import Flask, redirect, url_for
from flask_dance.consumer.storage import MemoryStorage
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github

@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    storage = MemoryStorage({"access_token": "client_secret"})
    monkeypatch.setattr(blueprint, 'storage', storage)      
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
    # Create the new app.
        test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    # Replace requests.get(url) with our own function
    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200