from utils.data import DataManagerInterface


class MockDataManager(DataManagerInterface):
    def __init__(self):
        self.data = []

    def load_data(self):
        return self.data

    def save_data(self, books):
        self.data = books
