from src.core.exceptions import NotFoundException, ConflictException


class CategoryNotFoundException(NotFoundException):
    """Category not found exception."""
    
    detail: str = "Category not found."


class CategoryConflictException(ConflictException):
    """Category conflict exception."""
    
    detail: str = "Category already exists." 