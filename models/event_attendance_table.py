from app import db

event_attendance = db.Table('event_attendance',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id'))
)