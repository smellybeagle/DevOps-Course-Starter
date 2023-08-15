
from todo_app.data.item import Item
from todo_app.view_model import ViewModel


def test_view_model_todos_method_only_returns_todo_items_and_not_other_statuses():
    # Arrange
    todo_items = [Item("1", "A todo I just created", "To Do")]
    doing_items = [Item("2", "A todo I created awhile ago", "In Progress")]
    done_items = [Item("3", "A todo I finished ages ago", "Completed")]
    
    view_model = ViewModel(todo_items, doing_items, done_items)
    
    # Act
    items = view_model.todos
    
    # Assert
    assert len(items) == 1
    single_item = items[0]
    assert single_item.status == "To Do"
    