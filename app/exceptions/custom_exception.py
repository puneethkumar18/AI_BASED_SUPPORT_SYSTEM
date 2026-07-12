

class TicketNotFoundException(Exception):
    def __init__(self):
        self.message = "Ticket not found."


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User not found."

class KnowledgeNotFoundException(Exception):
    def __init__(self):
        self.message = "Knowledge article not found."
