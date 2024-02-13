from todo_app.data.item import Item
from todo_app.debugger import writelog



class ViewModel:
    def __init__(self, todo_items: list[Item], doing_items: list[Item], done_item: list[Item]):
        self._items: list[Item] = todo_items + doing_items + done_item
 
    @property
    def todos(self) -> list[Item]:
        output: list[Item] = []   
        for item in self._items:
            if item.Status == "To Do":
                output.append(item)
        return output
    
    @property
    def doings(self) -> list[Item]:
        output: list[Item] = []   
        for item in self._items:
            if item.Status == "In Progress":
               output.append(item)
        return output
    
    @property
    def dones(self) -> list[Item]:
        output: list[Item] = []   
        for item in self._items:
            if item.Status == "Completed":
                output.append(item)
        return output