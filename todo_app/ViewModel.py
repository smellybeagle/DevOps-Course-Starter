from todo_app.trello_items import Item

class ViewModel:
    def __init__(self, todo_items: list[Item], doing_items: list[Item], done_items: list[Item]):
        self._items: list[Item] = todo_items + doing_items + done_items
 
    @property
    def todos(self):
        return self._items
    
    @property
    def doings(self):
        return self._items
    
    
    @property
    def dones(self):
        return self._items