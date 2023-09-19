from models.demo_model import Demo
from utilities.custom_exception_factory import CustomExceptionFactory

def get_message():
    return Demo.get_all_message()

# def add_message(data):
#     message = data['message']

#     if Demo.check_message_exists(message):
#         raise CustomExceptionFactory().create_exception('message_exists')
#     else:
#         return Demo.create(message=message)

def update_message(data):
    id = data['id']
    message = data['message']
    demo_instance = Demo.get_message(id)

    if demo_instance is None:
        raise CustomExceptionFactory().create_exception('id_not_found')
    elif Demo.check_message_exists(message):
        raise CustomExceptionFactory().create_exception('message_exists')
    else:
        demo_instance.update(message)

def delete_message(data):
    demo_instance = Demo.get_message(data['id'])

    if demo_instance is None:
        raise CustomExceptionFactory().create_exception('id_not_found')
    else:
        demo_instance.delete()