import os, requests
from flask import request
import json
#from flask import session


trello_key = os.getenv("API_KEY")
trello_token = os.getenv("TOKEN")
trello_board_id = os.getenv("BOARD_ID")
trello_list_id = os.getenv("LIST_ID")
#trello_url = os.getenv("BASE_URL")
trello_url = "https://api.trello.com/1/"
new_card_url="https://api.trello.com/1/cards/"

#trello_url_params = {"key": trello_key, "token": trello_token}

url1 = 'https://api.trello.com/1/boards/649be24fcd4e7f514a246cb9/lists'
url2= 'https://api.trello.com/1/lists/'
payload = {'key': trello_key, 'token': trello_token, 'field': 'name'}


response = requests.get(url1, params=payload)
data = response.content
data_dict=json.loads(data)

#print(data_dict)
# print(data_dict[0])
# print(data_dict[1])
# print(data_dict[1])

todo= data_dict[0].get("id");
doing= data_dict[1].get("id");
done= data_dict[2].get("id");

#print (todo)



urldoing = url2 + doing + '/cards'
payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
response1 = requests.get(urldoing, params=payload1)
ddoing = response1.content
dictdoing=json.loads(ddoing)

urldone = url2 + done + '/cards'
payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
response2 = requests.get(urldone, params=payload1)
ddone = response2.content
dictdone=json.loads(ddone)

# print (urltodo)
# print (urldoing)
# print (urldone)

#print(dicttodo[0].get("id"));
# print(dicttodo[1])
# print(dictdoing[0])
# print(dictdoing[1])
#print(dictdone)
#print (dicttodo)
def todolists():
  urltodo = url2 + todo + '/cards'
  payload1 = {'key': trello_key, 'token': trello_token, 'fields': 'name'}
  response = requests.get(urltodo, params=payload1)
  dtodo = response.content
  dicttodo=json.loads(dtodo)
  return dicttodo

def doinglists():
   return dictdoing

def donelists():
   return dictdone

#print(dictdoing)
headers = {"Accept": "application/json"}

def new_card():
     url = new_card_url
     name = request.form.get('name')
     query_params = {"idList": todo,"key": trello_key, "token": trello_token, "name" : name, "pos" : 'bottom'}
     #print(f"URL: {url}")
     requests.request("POST",url, headers=headers, params=query_params)
     #print(response.text)

def move_done():
     url3 = 'https://api.trello.com/1/cards/' 
     #name = request.form.get('new-todo')
     query_params = {"idList": todo,"key": trello_key, "token": trello_token}
     print(f"URL: {url3}")
     requests.request("PUT",url3, headers=headers, params=query_params)
     #print(response.text)