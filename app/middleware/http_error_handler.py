import requests
from typing import Dict, Type, Callable
from fastapi import HTTPException, status
from functools import wraps
from app.middleware.exception import *
from app.core.logger import ServiceLogger


logger = ServiceLogger(__name__)


class HTTPErrorHandler:
    ERROR_MAPPINGS: Dict[Type[Exception], int] = {
        requests.exceptions.ConnectionError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        requests.exceptions.Timeout: status.HTTP_408_REQUEST_TIMEOUT,
        requests.exceptions.RequestException: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ValueError: status.HTTP_400_BAD_REQUEST,
        EntityNotFoundException: status.HTTP_404_NOT_FOUND,
        EntityAlreadyExistsException: status.HTTP_409_CONFLICT,
        ValidationException: status.HTTP_422_UNPROCESSABLE_ENTITY,
        BusinessRuleException: status.HTTP_400_BAD_REQUEST,
        StatusException: status.HTTP_400_BAD_REQUEST,
        OperationException: status.HTTP_400_BAD_REQUEST,
        Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    @classmethod
    def handle_exceptions(cls, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Callable:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                err_class = e.__class__
                logger.error(
                    f"Error in {func.__name__}: {e}",
                    exc_info=e,
                    extra={
                        "error_type": err_class.__name__,
                        "endpoint": func.__name__,
                    }
                )
                
                status_code = cls.ERROR_MAPPINGS.get(err_class, status.HTTP_422_UNPROCESSABLE_ENTITY)

                raise HTTPException(
                    status_code=status_code,
                    detail=cls.format_error(e)
                ) from e
        return wrapper
    
    @staticmethod
    def format_error(e: Exception) -> Dict:
        return {
            "success": False,
            "message": str(e),
            "error_type": e.__class__.__name__,
        }
        
