
class BaseServiceException(Exception):
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundException(BaseServiceException):
    def __init__(self, entity_type: str, identifier: str = None):
        message = f"{entity_type} with identifier {identifier} not found"
        if identifier:
            message += f"{entity_type} with identifier {identifier} not found"
        super().__init__(
            message=message,
            code="ENTITY_NOT_FOUND",
            details={
                "identifier": identifier,
                "entity_type": entity_type
            }
        )

class EntityAlreadyExistsException(BaseServiceException):
    def __init__(self, entity_type: str, identifier: str):
        message = f"{entity_type} with identifier {identifier} already exists"
        super().__init__(
            message=message,
            code="ENTITY_ALREADY_EXISTS",
            details={
                "identifier": identifier,
                "entity_type": entity_type
            }
        )


class ValidationException(BaseServiceException):
    """Raised when validation fails"""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"errors": errors or {}}
        )


class OperationException(BaseServiceException):
    """Raised when an operation fails"""
    def __init__(self, operation: str, message: str, details: dict = None):
        super().__init__(
            message=message,
            code="OPERATION_ERROR",
            details={
                "operation": operation,
                **(details or {})
            }
        )


class StatusException(BaseServiceException):
    """Raised when an invalid status transition is attempted"""
    def __init__(self, entity_type: str, current_status: str, target_status: str):
        super().__init__(
            message=f"Invalid status transition for {entity_type}: {current_status} -> {target_status}",
            code="INVALID_STATUS",
            details={
                "entity_type": entity_type,
                "current_status": current_status,
                "target_status": target_status
            }
        )


class BusinessRuleException(BaseServiceException):
    """Raised when a business rule is violated"""
    def __init__(self, rule: str, message: str, details: dict = None):
        super().__init__(
            message=message,
            code="BUSINESS_RULE_VIOLATION",
            details={
                "rule": rule,
                **(details or {})
            }
        )

