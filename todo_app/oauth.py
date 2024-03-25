import os
from flask import session
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer import oauth_authorized

blueprint = make_github_blueprint(
    client_id = os.getenv('OAUTH_CLIENT_ID'),
    client_secret = os.getenv('OAUTH_CLIENT_SECRET'),
    
)
def get_role_for_user(username):
    # Should return 'writer' if user_id matches your GitHub id
    # And 'reader' if not
    username=session["username"]
    if username == os.getenv("OAUTHADMIN"):
        role="ADMIN"
    else:
        role="READ ONLY" 
    return role

@oauth_authorized.connect
def github_logged_in(blueprint, token):
    
    # Use the blueprint to make a request to GitHub to get the user details
    response = blueprint.session.get("/user")
    user_dict = response.json()
    session["username"]=user_dict.get("login")
    session["role"] = get_role_for_user(session["username"])
    return session
    # Return False to have Flask-Dance forget the token as we won't use it again
    #return False

