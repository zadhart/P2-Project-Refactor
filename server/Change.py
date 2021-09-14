from create_app import db

class Change():
    def __init__(self, new_data, prev_data):
        self.prev_data = prev_data
        self.new_data = new_data

    def undo(self):
        obj = self.prev_data
        db.session.delete(obj)
        db.session.commit()
