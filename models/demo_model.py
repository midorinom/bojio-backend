from app import db
from dataclasses import dataclass

@dataclass
class Demo(db.Model):
    __tablename__ = 'demo'
    id:int = db.Column(db.Integer, primary_key = True)
    message:str = db.Column(db.String(200), nullable = False)
    
    def __init__(self, message):
        self.message = message

    @classmethod
    def check_message_exists(cls, message):
        return True if cls.query.filter_by(message=message).first() is not None else False
    
    @classmethod
    def get_message(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all_message(cls):
        return cls.query.all()

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.flush()
        db.session.refresh(obj) # Refresh object so it will have the new ID
        return (obj)

    def update(self, new_message):
        self.message = new_message
        db.session.flush()

    def delete(self):
        db.session.delete(self)
        db.session.flush()