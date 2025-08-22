class DomainError(Exception):
    pass

class ValidationError(DomainError):
    pass

class NotFoundError(DomainError):
    pass
