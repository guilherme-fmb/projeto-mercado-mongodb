from pymongo import MongoClient

class DatabaseConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="supermercado"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]