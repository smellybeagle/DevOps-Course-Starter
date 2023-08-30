import json
import os
from typing import Any
from dotenv import load_dotenv, find_dotenv
from flask.testing import FlaskClient
import pytest
import requests
from todo_app import app

#from todo_app.app import create_app



@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    monkeypatch.setattr(requests, 'get', stub)
    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
        self.content=json.dumps(fake_response_data)

    def json(self):
        return self.fake_response_data

# Stub replacement for requests.get(url)
def stub(url, params={}):
    #test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/a123b456c789d0/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'status': 'To Do'
        },{'id': '123abcd',
            'name': 'Doing',
            'status': 'In Progress'}
        ,{'id': '123abcde',
            'name': 'Done',
            'status': 'Completed'}]
        return StubResponse(fake_response_data)
    if url == f'https://api.trello.com/1/lists/a123b456c789d012xy1/cards':
        fake_response_data = [{
            'id': '1234567',
            'name': 'Sample new todo card',
            'status': 'To Do'
        }]
        return StubResponse(fake_response_data)
    if url == f'https://api.trello.com/1/lists/a123b456c789d012xy2/cards':
        fake_response_data = [{
            'id': '12345678',
            'name': 'Sample Moved to InProgress',
            'status': 'In Progress'
        }]
        return StubResponse(fake_response_data)
    if url == f'https://api.trello.com/1/lists/a123b456c789d012xy3/cards':
        fake_response_data = [{
            'id': '123456789',
            'name': 'Sample Moved Completed',
            'status': 'Completed'
        }]
        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    # Replace requests.get(url) with our own function

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    #assert 'Test card' in response.data.decode()