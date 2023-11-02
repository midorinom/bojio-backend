from app import db
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Event(db.Model):
    __tablename__ = 'events'
    id:int = db.Column(db.Integer, primary_key = True)
    host_id:int = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    title:str = db.Column(db.String(200), nullable = False)
    description:str = db.Column(db.Text, nullable = False)
    start_date:datetime = db.Column(db.Date, default = datetime.utcnow, nullable = False)
    end_date:datetime = db.Column(db.Date, default = datetime.utcnow, nullable = False)
    location:str = db.Column(db.Text, nullable = False)
    capacity:int = db.Column(db.Integer, nullable = False)
    price:Decimal = db.Column(db.Numeric(10, 2), nullable = False)

    def __init__(self, host, title, description, start_date, end_date, location, capacity, price):
        self.host = host
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.capacity = capacity
        self.price = price
    
    @classmethod
    def get_event(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_all_events(cls):
        return cls.query.all()

    @classmethod
    def create_event(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.flush()
        db.session.refresh(obj) # Refresh object so it will have the new ID
        return (obj)
    
    def update(self, event_with_updates):
        self.title = event_with_updates['title']
        self.description = event_with_updates['description']
        self.start_date = event_with_updates['start_date']
        self.end_date = event_with_updates['end_date']
        self.location = event_with_updates['location']
        self.capacity = event_with_updates['capacity']
        self.price = event_with_updates['price']
        db.session.flush()

    def delete(self):
        db.session.delete(self)
        db.session.flush()
