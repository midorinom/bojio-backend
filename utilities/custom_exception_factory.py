# Demo exceptions
class DemoMessageExistsException(Exception):
    def __init__(self, message='Message exists already'):
        super(DemoMessageExistsException, self).__init__(message)

# User exceptions
class UserNotFoundException(Exception):
    def __init__(self, message='User cannot be found'):
        super(UserNotFoundException, self).__init__(message)

class UserNotLoggedInException(Exception):
    def __init__(self, message='user_not_logged_in'):
        super(UserNotLoggedInException, self).__init__(message)

# Event exceptions
class EventNotFoundException(Exception):
    def __init__(self, message='event_not_found'):
        super(EventNotFoundException, self).__init__(message)

class AlreadyAttendingException(Exception):
    def __init__(self, message='already_attending_event'):
        super(AlreadyAttendingException, self).__init__(message)

class AlreadyWithdrawnException(Exception):
    def __init__(self, message='already_withdrawn'):
        super(AlreadyWithdrawnException, self).__init__(message)

class UserIsNotHostException(Exception):
    def __init__(self, message='User is not the host for this event'):
        super(UserIsNotHostException, self).__init__(message)

class UserIsHostException(Exception):
    def __init__(self, message='user_is_host'):
        super(UserIsHostException, self).__init__(message)

class EventAtMaxCapacityException(Exception):
    def __init__(self, message='event_at_max_capacity'):
        super(EventAtMaxCapacityException, self).__init__(message)

class InvitorIsAlsoInviteeException(Exception):
    def __init__(self, message='User cannot invite themselve'):
        super(InvitorIsAlsoInviteeException, self).__init__(message)

class InviteeAlreadyReceivedException(Exception):
    def __init__(self, message='Invitee already received user\'s invite'):
        super(InviteeAlreadyReceivedException, self).__init__(message)

class InviteeIsHostException(Exception):
    def __init__(self, message='Invitee is the event\'s host'):
        super(InviteeIsHostException, self).__init__(message)

# Generic exceptions
class IdNotFoundException(Exception):
    def __init__(self, message='ID cannot be found'):
        super(IdNotFoundException, self).__init__(message)

class CustomExceptionFactory:
    def create_exception(self, exception_type):
        match exception_type:
            case 'id_not_found':
                return IdNotFoundException()
            case 'demo_message_exists':
                return DemoMessageExistsException()
            case 'user_not_found':
                return UserNotFoundException()
            case 'user_not_logged_in':
                return UserNotLoggedInException()
            case 'event_not_found':
                return EventNotFoundException()
            case 'already_attending':
                return AlreadyAttendingException()
            case 'already_withdrawn':
                return AlreadyWithdrawnException()
            case 'user_is_not_host':
                return UserIsNotHostException()
            case 'user_is_host':
                return UserIsHostException()
            case 'event_at_max_capacity':
                return EventAtMaxCapacityException()
            case 'invitor_is_also_invitee':
                return InvitorIsAlsoInviteeException()
            case 'invitee_already_received':
                return InviteeAlreadyReceivedException()
            case 'invitee_is_host':
                return InviteeIsHostException()