from src.core.exceptions import NotFoundException, ConflictException


class ProductNotFoundException(NotFoundException):
    """Product not found exception."""
    
    detail: str = "Product not found."


class ProductConflictException(ConflictException):
    """Product conflict exception."""
    
    detail: str = "Product already exists." 