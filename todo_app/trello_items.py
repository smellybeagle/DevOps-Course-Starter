import os, requests
from flask import request

# trello_key = os.getenv("TRELLO_API")
# trello_token = os.getenv("TRELLO_TOKEN")
# trello_board_id = os.getenv("TRELLO_BOARD")
# trello_url = os.getenv("BASE_URL")
trello_key = os.getenv("API_KEY")
trello_token = os.getenv("TOKEN")
trello_board_id = os.getenv("BOARD_ID")
trello_list_id = os.getenv("LIST_ID")
#trello_url = os.getenv("BASE_URL")
trello_url = "https://api.trello.com/1/"
new_card_url="https://api.trello.com/1/cards"

#trello_url_params = {"key": trello_key, "token": trello_token}

headers = {"Accept": "application/json"}

def get_lists():
    get_lists_path = "boards/"+trello_board_id+"/lists"
    url = trello_url + get_lists_path
    query_params = {"key": trello_key, "token": trello_token, "cards": "open", "card_fields": "id,name,shortUrl"}
    #query_params = {"key": trello_key, "token": trello_token, "cards": "open", "card_fields": "name"}
    print(f"URL: {url}")
    response = requests.get(url, headers=headers, params=query_params)
    #response = requests.get(url, params=query_params)
    #print("JSON response is...")
    print(response.json())
    response_json = response.json()
      

    cards_dict = []
    for trello_list in response_json:

        for each_card in trello_list['cards']:

            cards_dict.append(each_card)

    print("JSON (cards_dict) response is...")
    print(cards_dict)

    return cards_dict

def new_card():
    url = new_card_url
    #name = request.form.get('new-todo')
    query_params = {"idList": trello_list_id,"key": trello_key, "token": trello_token, "name" : request.form.get('new-todo')}
    print(f"URL: {url}")
    requests.request("POST",url, headers=headers, params=query_params)
    #print(response.text)
