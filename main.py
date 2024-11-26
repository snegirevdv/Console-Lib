#!/usr/bin/env python3

from services.library import LibraryService
from utils.data import JsonManager
from cli import ConsoleUI


def main():
    data_manager = JsonManager()
    library_service = LibraryService(data_manager)
    cli = ConsoleUI(library_service)
    cli.run()


if __name__ == "__main__":
    main()
