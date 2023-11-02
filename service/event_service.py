from models.event_model import Event
from models.user_model import User
from utilities.custom_exception_factory import CustomExceptionFactory
from flask import session

# Business logic lies here

def get_all_events():
    if 'loggedin' in session:
        user_id = session['id']
        events = Event.get_all_events()
        user = User.get_user(user_id)

        events_list = []

        for event in events:
            event_obj = {
                "id": event.id,
                "host_id": event.host.user_id,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "location": event.location,
                "capacity": event.capacity,
                "price": event.price,
                "attending": False
            }
            
            if event in user.events_as_attendee:
                event_obj['attending'] = True
            elif event in user.events_as_host:
                event_obj['attending'] = 'Host'
            
            events_list.append(event_obj)

        return events_list
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def create_event(new_event):
    if 'loggedin' in session:
        return Event.create_event(
            host = User.get_user(session['id']),
            title = new_event['title'],
            description = new_event['description'],
            start_date = new_event['start_date'],
            end_date = new_event['end_date'],
            location = new_event['location'],
            capacity = new_event['capacity'],
            price = new_event['price']
        )
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def update_event(event_with_updates):
    if 'loggedin' in session:
        event_id = event_with_updates['id']
        event_without_updates = Event.get_event(event_id)

        if event_without_updates.host.user_id != session['id']:
            raise CustomExceptionFactory().create_exception('user_is_not_host')
        elif event_without_updates is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        else:
            event_without_updates.update(event_with_updates)
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def delete_event(data):
    if 'loggedin' in session:
        event_id = data['event_id']
        event_instance = Event.get_event(event_id)

        if event_instance.host.user_id != session['id']:
            raise CustomExceptionFactory().create_exception('user_is_not_host')
        if event_instance is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        else:
            event_instance.delete()
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def join_event(data):
    if 'loggedin' in session:
        user_id = data['user_id']
        event_id = data['event_id']
        user = User.get_user(user_id)
        event = Event.get_event(event_id)

        if user is None:
            raise CustomExceptionFactory().create_exception('user_not_found')
        elif event is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event in user.events_as_attendee:
            raise CustomExceptionFactory().create_exception('already_attending')
        else:
            user.events_as_attendee.append(event)
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def quit_event(data):
    if 'loggedin' in session:
        user_id = data['user_id']
        event_id = data['event_id']
        user = User.get_user(user_id)
        event = Event.get_event(event_id)

        if user is None:
            raise CustomExceptionFactory().create_exception('user_not_found')
        elif event is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event not in user.events_as_attendee:
            raise CustomExceptionFactory().create_exception('already_withdrawn')
        else:
            user.events_as_attendee.remove(event)
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')