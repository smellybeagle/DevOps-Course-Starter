class Item:
    def __init__(self, _id, name, desc,Status):
        self._id = _id
        self.name = name
        self.desc = desc
        self.Status = Status

    @classmethod
    def from_mongo(cls, card):
        return cls(card['_id'], card['name'], card['desc'],card['Status'])