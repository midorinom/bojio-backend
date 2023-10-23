from models.event_model import Event
from utilities.custom_exception_factory import CustomExceptionFactory

# Business logic lies here

def create_event(data):
    host_id = data['host_id']
    title = data['title']
    description = data['description']
    start_date = data['start_date']
    end_date = data['end_date']
    location = data['location']
    capacity = data['capacity']
    price = data['price']

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