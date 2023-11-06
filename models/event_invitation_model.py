from app import db
from dataclasses import dataclass

@dataclass
class EventInvitation(db.Model):
    __tablename__ = 'event_invitations'
    invitation_id:int = db.Column(db.Integer, primary_key = True)
    inviter_id:int = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    invitee_id:int = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    event_id:int = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable = False)
    
    def __init__(self, inviter_id, invitee_id, event_id):
        self.inviter_id = inviter_id
        self.invitee_id = invitee_id
        self.event_id = event_id
    
    @classmethod
    def create_invitation(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.flush()
        # db.session.refresh(obj) # Refresh object so it will have the new ID
        # return (obj)