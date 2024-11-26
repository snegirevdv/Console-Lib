#!/usr/bin/env python3

from services.library import LibraryService
from utils.data import JsonManager
from cli import ConsoleInterface


def main():
    data_manager = JsonManager()
    library_service = LibraryService(data_manager)
    cli = ConsoleInterface(library_service)
    cli.run()


if __name__ == "__main__":
    main()
