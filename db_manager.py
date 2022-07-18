from datetime import datetime

from pymongo import MongoClient


class DBManager:
    def __init__(self, mongodb_url):
        self.client = MongoClient(mongodb_url)

        self.db = self.client.admin
        self.parking_collection = self.db['Parking']

    def add_decision_to_database(self, plate_number, is_approved, category):
        utcnow = datetime.utcnow()
        self.parking_collection.insert_one(
            {"Plate Number": plate_number, "Decision": is_approved, "Category": category, "timestamp": utcnow})

