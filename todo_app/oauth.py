import os
import functools
from flask import flash
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer import oauth_authorized

blueprint = make_github_blueprint(
    client_id = os.getenv('OAUTH_CLIENT_ID'),
    client_secret = os.getenv('OAUTH_CLIENT_SECRET'),
    
)