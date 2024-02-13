from todo_app.data.item import Item
from todo_app.view_model import ViewModel
from todo_app.debugger import writelog


def test_view_model_todos_method_only_returns_todo_items_and_not_other_statuses():
    # Arrange
    todo_items = [Item("1", "A todo I just created", '',"To Do")]
    doing_items = [Item("2", "A todo I created awhile ago", '',"In Progress")]
    done_items = [Item("3", "A todo I finished ages ago",'', "Completed")]
    
    view_model = ViewModel(todo_items, doing_items, done_items)
    
    # Act
    tditems = view_model.todos
    doitems = view_model.doings
    dnitems = view_model.dones
    # Assert
    assert len(tditems) == 1
    single_tditem = tditems[0]
    assert single_tditem.Status == "To Do"
    
    assert len(doitems) == 1
    single_doitem = doitems[0]
    assert single_doitem.Status == "In Progress"
    
    assert len(dnitems) == 1
    single_dnitem = dnitems[0]
    assert single_dnitem.Status == "Completed"