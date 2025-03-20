from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base exception for all API exceptions."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred."
    
    def __init__(self, detail: str = None):
        """Initialize with optional custom detail message."""
        super().__init__(
            status_code=self.status_code, 
            detail=detail or self.detail
        )


class NotFoundException(APIException):
    """Exception for resource not found."""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."


class ConflictException(APIException):
    """Exception for resource conflict."""
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists."


class ValidationException(APIException):
    """Exception for validation errors."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation error."


class UnauthorizedException(APIException):
    """Exception for unauthorized access."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized access."


class ForbiddenException(APIException):
    """Exception for forbidden access."""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden access."


class BadRequestException(APIException):
    """Exception for bad request."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request."


class ServerException(APIException):
    """Exception for server error."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error."


def configure_exception_handlers(app):
    """Configure exception handlers for the application."""
    
    @app.exception_handler(APIException)
    async def custom_exception_handler(request, exc):
        from fastapi.responses import JSONResponse
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        ) 