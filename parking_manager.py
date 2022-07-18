import os
import re

import cherrypy

from db_manager import DBManager
from ocr_space import OcrSpace

mongodb_url = 'mongodb://localhost:27017'



class Category:
    PUBLIC_TRANSPORTATION = "Public Transportation"
    SEVEN_DIGITS_DECLINED = "Seven Digits Declined"
    TWO_DIGITS_DECLINED_POSTFIX = "Two Digits Declined Postfix"


class ParkingManager:
    def __init__(self, api_key):
        self.ocr_space = OcrSpace(api_key)
        self.db_manager = DBManager(mongodb_url)
        # I've assumed that 7 digit plate number that ends with 25 is prohibited to enter the parking lot
        self.access_decline_postfix = ("85", "86", "87", "88", "89", "00")
        self.access_decline_7_digits = ("0", "5")
        self.access_approve_postfix = ("25", "26")

    @cherrypy.expose
    def index(self):
        # Ask for the user's name.
        return '''
                  <form action="greetUser" method="GET">
                  </form>'''

    def extract_license_plate_number(self, file_image):
        parsed_result_json = self.ocr_space.ocr_space_file(filename=file_image)
        parsed_result = re.search(pattern="\"ParsedText\":\"(.*?)\"", string=parsed_result_json).group(1)
        number = ''.join(c for c in parsed_result if c.isdigit())
        return number

    @cherrypy.expose
    def is_car_approved_to_access(self, file_image):
        plate_number = self.extract_license_plate_number(file_image=file_image)

        if (plate_number.endswith(self.access_decline_postfix)):
            self.report_decision_to_db(plate_number=plate_number, is_approved=False,
                                       category=Category.TWO_DIGITS_DECLINED_POSTFIX)
            print("Declined")

        if (len(plate_number) == 7 and plate_number.endswith(self.access_decline_7_digits)):
            self.report_decision_to_db(plate_number=plate_number, is_approved=False,
                                       category=Category.SEVEN_DIGITS_DECLINED)
            print("Declined")

        if (plate_number.endswith(self.access_approve_postfix)):
            self.report_decision_to_db(plate_number=plate_number,
                                       is_approved=True, category=Category.PUBLIC_TRANSPORTATION)
            print("Approved")

    def report_decision_to_db(self, plate_number, is_approved, category):
        self.db_manager.add_decision_to_database(plate_number=plate_number, is_approved=is_approved, category=category)


tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':

    cherrypy.quickstart(ParkingManager(api_key="K89032823888957"), config=tutconf)
