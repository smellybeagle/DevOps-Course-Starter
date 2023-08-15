import os, requests
from flask import request
import json

from todo_app.data.item import Item

# declare variables that will be later set & used elsewhere
trello_key, trello_token, trello_board_id, trello_list_id = None, None, None, None
todo, doing, done = None, None, None
url1 = ""

new_card_url="https://api.trello.com/1/cards/"
url2= 'https://api.trello.com/1/lists/'

def init_trello():
  # declare which variables from outside the function we'll be changing
  global trello_key, trello_board_id, trello_token, trello_list_id,trello_url,new_card_url, url1,url2,envtodo,envdoing,envdone
  global todo, doing, done
  trello_key = os.getenv("API_KEY")
  trello_token = os.getenv("TOKEN")
  trello_board_id = os.getenv("BOARD_ID")
  envtodo = os.getenv("TODO_LIST_ID")
  envdoing = os.getenv("DOING_LIST_ID")
  envdone = os.getenv("DONE_LIST_ID")
  trello_url = "https://api.trello.com/1/"
  new_card_url="https://api.trello.com/1/cards/"
  url1 = 'https://api.trello.com/1/boards/' + trello_board_id +'/lists'
  url2= 'https://api.trello.com/1/lists/'
  payload = {'key': trello_key, 'token': trello_token, 'field': 'name'}


  response = requests.get(url1, params=payload)
  data = response.content
  data_dict=json.loads(data)

  todo= data_dict[0].get("id");
  doing= data_dict[1].get("id");
  done= data_dict[2].get("id");

# response = requests.get(url1, params=payload)
# data = response.content
# data_dict=json.loads(data)

#todo= data_dict[0].get("id"); 
#doing= data_dict[1].get("id");
#done= data_dict[2].get("id");



def todolists():
  urltodo = url2 + envtodo + '/cards'
  payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
  response = requests.get(urltodo, params=payload1)
  dtodo = response.content
  dicttodo=json.loads(dtodo)
  todos = []
  for todo_item in dicttodo:
      todos.append(Item.from_trello_card(todo_item, "To Do"))
  return todos


def doinglists():
  urldoing = url2 + envdoing + '/cards'
  payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
  response = requests.get(urldoing, params=payload1)
  dddoing = response.content
  dictdoing=json.loads(dddoing)
  doing = []
  for doing_item in dictdoing:
      doing.append(Item.from_trello_card(doing_item, "In Progress"))
  return doing


def donelists():
  urldone = url2 + envdone + '/cards'
  payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
  response = requests.get(urldone, params=payload1)
  ddone = response.content
  dictdone=json.loads(ddone)
  done = []
  for done_item in dictdone:
      done.append(Item.from_trello_card(done_item, "Completed"))
  return done


headers = {"Accept": "application/json"}

def new_card():
     url = new_card_url
     name = request.form.get('name')
     query_params = {"idList": envtodo,"key": trello_key, "token": trello_token, "name" : name, "pos" : 'bottom'}
     requests.request("POST",url, headers=headers, params=query_params)


def move_doing():
     trelloid = request.form.get('id')
     url3 = 'https://api.trello.com/1/cards/' + trelloid
     query_params = {"idList": envdoing,"key": trello_key, "token": trello_token}
     print(f"URL: {url3}")
     requests.request("PUT",url3, headers=headers, params=query_params)


def move_done():
     trelloid = request.form.get('id')
     url3 = 'https://api.trello.com/1/cards/' + trelloid 
     query_params = {"idList": envdone,"key": trello_key, "token": trello_token}
     print(f"URL: {url3}")
     requests.request("PUT",url3, headers=headers, params=query_params)