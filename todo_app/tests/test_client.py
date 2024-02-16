import json
from dotenv import load_dotenv, find_dotenv
from flask.testing import FlaskClient
import pytest
import mongomock
from todo_app import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
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
    fake_response_data = None
    if url == f'https://localhost:5000':
        fake_response_data = [{
            '_id': '123abc',
            'name': 'To Do',
            'desc': 'A basic To Do item',
            'Status': 'To Do'
        },{'_id': '123abcd',
            'name': 'Doing',
            'desc': 'A basic To Do item',
            'Status': 'In Progress'}
        ,{'_id': '123abcde',
            'name': 'Done',
            'desc': 'A basic To Do item',
            'Status': 'Completed'}]
        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    # Replace requests.get(url) with our own function

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200