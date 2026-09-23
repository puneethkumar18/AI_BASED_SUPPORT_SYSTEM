

class TicketNotFoundException(Exception):
    def __init__(self):
        self.message = "Ticket not found."


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User not found."

class CommentNotFoundException(Exception):
    def __init__(self):
        self.message = "Comment not found."

class KnowledgeNotFoundException(Exception):
    def __init__(self):
        self.message = "Knowledge article not found."

class LLMException(Exception):
    def __init__(self, message:str):
        self.message = message

class ValueErrorException(Exception):
    def __init__(self, message:str):
        self.message = message
