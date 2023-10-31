# Demo exceptions
class DemoMessageExistsException(Exception):
    def __init__(self, message='Message exists already'):
        super(DemoMessageExistsException, self).__init__(message)

# User exceptions
class UserNotFoundException(Exception):
    def __init__(self, message='User cannot be found'):
        super(UserNotFoundException, self).__init__(message)

# Event exceptions
class EventNotFoundException(Exception):
    def __init__(self, message='Event cannot be found'):
        super(EventNotFoundException, self).__init__(message)

class AlreadyAttendingException(Exception):
    def __init__(self, message='Already attending event'):
        super(AlreadyAttendingException, self).__init__(message)

class AlreadyWithdrawnException(Exception):
    def __init__(self, message='Already withdrawn from event'):
        super(AlreadyWithdrawnException, self).__init__(message)

# Generic exceptions
class IdNotFoundException(Exception):
    def __init__(self, message='ID cannot be found'):
        super(IdNotFoundException, self).__init__(message)

class CustomExceptionFactory:
    def create_exception(self, exception_type):
        match exception_type:
            case 'demo_message_exists':
                return DemoMessageExistsException()
            case 'id_not_found':
                return IdNotFoundException()
            case 'user_not_found':
                return UserNotFoundException()
            case 'event_not_found':
                return EventNotFoundException()
            case 'already_attending':
                return AlreadyAttendingException()
            case 'already_withdrawn':
                return AlreadyWithdrawnException()