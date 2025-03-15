NON_FIELD_ERRORS = 'non_field_errors'

class NotProjectMemberError(Exception):
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DuplicateProjectMemberError(Exception):
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
        