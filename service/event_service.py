from models.event_model import Event
from models.user_model import User
from utilities.custom_exception_factory import CustomExceptionFactory
from flask import session
from datetime import datetime

# Business logic lies here

def get_all_events():
    if 'loggedin' in session:
        user_id = session['id']
        events = Event.get_all_events()
        user = User.get_user(user_id)

        events_list = []

        for event in events:
            event_obj = {
                "event_id": event.event_id,
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
            # Only append events that is not hosted by current user
            if event not in user.events_as_host:
                if event in user.events_as_attendee:
                    event_obj['attending'] = True
            
                events_list.append(event_obj)

        return events_list
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def get_all_events_as_attendee():
    if 'loggedin' in session:
        user_id = session['id']
        events = Event.get_all_events()
        user = User.get_user(user_id)

        events_list = []

        for event in events:
            if event in user.events_as_attendee:
                events_list.append(event)

        return events_list
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def get_all_events_as_host():
    if 'loggedin' in session:
        user_id = session['id']
        events = Event.get_all_events()
        user = User.get_user(user_id)

        events_list = []

        for event in events:
            if event in user.events_as_host:
                events_list.append(event)

        return events_list
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def create_event(new_event):
    if 'loggedin' in session:
        host = User.get_user(session['id'])
        title = new_event['title'].strip()
        description = new_event['description'].strip()
        start_date = datetime.strptime(new_event['start_date'], '%d-%m-%Y')
        end_date = datetime.strptime(new_event['end_date'], '%d-%m-%Y')
        location = new_event['location'].strip()
        capacity = new_event['capacity']
        price = new_event['price']

        if not title or not description or not start_date or not end_date or not location or not capacity or not price:
            raise ValueError('Make sure all required fields are provided')
        elif start_date <= datetime.now() or end_date <= datetime.now():
            raise ValueError('Start and end date cannot be on or before today')
        elif not isinstance(capacity, int):
            raise ValueError('Capacity is not an integer')
        elif not str(price).isdecimal():
            raise ValueError('Price is not decimal')
        else:
            return Event.create_event(
                host = host,
                title = title,
                description = description,
                start_date = start_date,
                end_date = end_date,
                location = location,
                capacity = capacity,
                price = price
            )
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def update_event(event_with_updates):
    if 'loggedin' in session:
        event_id = event_with_updates['event_id']
        event_instance = Event.get_event(event_id)

        if event_instance is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event_instance.host.user_id != session['id']:
            raise CustomExceptionFactory().create_exception('user_is_not_host')
        else:
            title = event_with_updates['title'].strip()
            description = event_with_updates['description'].strip()
            start_date = datetime.strptime(event_with_updates['start_date'], '%d-%m-%Y')
            end_date = datetime.strptime(event_with_updates['end_date'], '%d-%m-%Y')
            location = event_with_updates['location'].strip()
            capacity = event_with_updates['capacity']
            price = event_with_updates['price']

            if not title or not description or not start_date or not end_date or not location or not capacity or not price:
                raise ValueError('Make sure all required fields are provided')
            elif start_date <= datetime.now() or end_date <= datetime.now():
                raise ValueError('Start and end date cannot be on or before today')
            elif not isinstance(capacity, int):
                raise ValueError('Capacity is not an integer')
            elif not str(price).isdecimal():
                raise ValueError('Price is not decimal')
            else:
                return event_instance.update(
                    title = title,
                    description = description,
                    start_date = start_date,
                    end_date = end_date,
                    location = location,
                    capacity = capacity,
                    price = price
                )
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def delete_event(event_id):
    if 'loggedin' in session:
        event_instance = Event.get_event(event_id)
        
        if event_instance is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event_instance.host.user_id != session['id']:
            raise CustomExceptionFactory().create_exception('user_is_not_host')
        else:
            event_instance.delete()
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def join_event(event_id):
    if 'loggedin' in session:
        user_id = session['id']
        user = User.get_user(user_id)
        event = Event.get_event(event_id)

        if event is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event.host.user_id == session['id']:
            raise CustomExceptionFactory().create_exception('user_is_host')
        elif event in user.events_as_attendee:
            raise CustomExceptionFactory().create_exception('already_attending')
        else:
            user.events_as_attendee.append(event)
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def quit_event(data):
    if 'loggedin' in session:
        user_id = session['id']
        event_id = data['event_id']
        user = User.get_user(user_id)
        event = Event.get_event(event_id)

        if event is None:
            raise CustomExceptionFactory().create_exception('event_not_found')
        elif event.host.user_id == session['id']:
            raise CustomExceptionFactory().create_exception('user_is_host')
        elif event not in user.events_as_attendee:
            raise CustomExceptionFactory().create_exception('already_withdrawn')
        else:
            user.events_as_attendee.remove(event)
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')