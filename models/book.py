from dataclasses import dataclass

from .status import BookStatus


@dataclass
class Book:
    """Модель книги."""

    id: int
    title: str
    author: str
    year: int
    status: str = BookStatus.AVAILABLE.value
