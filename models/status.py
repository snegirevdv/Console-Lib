from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "в наличии"
    BORROWED = "выдана"

    @classmethod
    def get_available_statuses(cls):
        return [status.value for status in cls]
