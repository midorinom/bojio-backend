from models.event_model import Event
from models.user_model import User
from utilities.custom_exception_factory import CustomExceptionFactory

# Business logic lies here

def get_all_events():
    return Event.get_all_events()

def create_event(new_event):
    host_id = new_event['host_id']
    title = new_event['title']
    description = new_event['description']
    start_date = new_event['start_date']
    end_date = new_event['end_date']
    location = new_event['location']
    capacity = new_event['capacity']
    price = new_event['price']

    return Event.create_event(
        host_id = host_id,
        title = title,
        description = description,
        start_date = start_date,
        end_date = end_date,
        location = location,
        capacity = capacity,
        price = price
    )

def update_event(event_with_updates):
    id = event_with_updates['id']
    event_without_updates = Event.get_event(id)
    
    if event_without_updates is None:
        raise CustomExceptionFactory().create_exception('id_not_found')
    else:
        event_without_updates.update(event_with_updates)

def delete_event(data):
    id = data['id']
    event_instance = Event.get_event(id)

    if event_instance is None:
        raise CustomExceptionFactory().create_exception('id_not_found')
    else:
        event_instance.delete()

def join_event(data):
    user_id = data['user_id']
    event_id = data['event_id']
    user = User.get_user(user_id)
    event = Event.get_event(event_id)

    if user is None:
        raise CustomExceptionFactory().create_exception('user_not_found')
    elif event is None:
        raise CustomExceptionFactory().create_exception('event_not_found')
    elif event in user.events:
        raise CustomExceptionFactory().create_exception('already_attending')
    else:
        user.events.append(event)

def quit_event(data):
    user_id = data['user_id']
    event_id = data['event_id']
    user = User.get_user(user_id)
    event = Event.get_event(event_id)

    if user is None:
        raise CustomExceptionFactory().create_exception('user_not_found')
    elif event is None:
        raise CustomExceptionFactory().create_exception('event_not_found')
    elif event not in user.events:
        raise CustomExceptionFactory().create_exception('already_withdrawn')
    else:
        user.events.remove(event)