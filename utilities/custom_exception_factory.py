# Demo exceptions
class DemoMessageExistsException(Exception):
    def __init__(self, message='Message exists already'):
        super(DemoMessageExistsException, self).__init__(message)

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