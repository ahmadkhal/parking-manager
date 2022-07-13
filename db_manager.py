from datetime import datetime

from pymongo import MongoClient


class DBManager:
    def __init__(self, mongodb_url):
        self.client = MongoClient(mongodb_url)

        self.db = self.client.admin
        self.parking_collection = self.db['Parking']

    def add_decision_to_database(self, plate_number, is_approved):
        utcnow = datetime.utcnow()
        res = self.parking_collection.insert_one(
            {"plate number": plate_number, "decision": is_approved, "date": utcnow, "time": datetime.timestamp(utcnow)})
        cursor = self.parking_collection.find({})
        for doc in cursor:
            print(doc)



