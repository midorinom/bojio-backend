class MessageExistsException(Exception):
    def __init__(self, message='Message exists already'):
        super(MessageExistsException, self).__init__(message)

class IdNotFoundException(Exception):
    def __init__(self, message='Id cannot be found'):
        super(IdNotFoundException, self).__init__(message)

class CustomExceptionFactory:
    def create_exception(self, exception_type):
        match exception_type:
            case 'message_exists':
                return MessageExistsException()
            case 'id_not_found':
                return IdNotFoundException()